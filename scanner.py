
import re
import subprocess


def scan_wifi_networks():
    """Scan nearby Wi-Fi networks using Windows netsh."""

    try:
        result = subprocess.run(
            [
                "netsh",
                "wlan",
                "show",
                "networks",
                "mode=bssid",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=25,
            check=False,
        )

        output = result.stdout + "\n" + result.stderr
        lowered = output.lower()

        if "requires elevation" in lowered:
            raise RuntimeError(
                "Windows requires administrator permission "
                "to read Wi-Fi information."
            )

        if "location permission" in lowered:
            raise RuntimeError(
                "Enable Windows Location services in "
                "Settings > Privacy & security > Location."
            )

        if result.returncode != 0:
            raise RuntimeError(
                output.strip() or "Windows Wi-Fi scan failed."
            )

        networks = []
        current = None

        for raw_line in result.stdout.splitlines():
            line = raw_line.strip()

            ssid_match = re.match(
                r"^SSID\s+\d+\s*:\s*(.*)$", line
            )

            if ssid_match:
                if current is not None:
                    networks.append(current)

                current = {
                    "ssid": (
                        ssid_match.group(1).strip()
                        or "<Hidden network>"
                    ),
                    "authentication": "Unknown",
                    "encryption": "Unknown",
                    "signal": "Unknown",
                }
                continue

            if current is None:
                continue

            auth_match = re.match(
                r"^Authentication\s*:\s*(.*)$", line
            )
            encryption_match = re.match(
                r"^Encryption\s*:\s*(.*)$", line
            )
            signal_match = re.match(
                r"^Signal\s*:\s*(\d+)%", line
            )

            if auth_match:
                current["authentication"] = (
                    auth_match.group(1).strip()
                )

            if encryption_match:
                current["encryption"] = (
                    encryption_match.group(1).strip()
                )

            if signal_match:
                current["signal"] = int(
                    signal_match.group(1)
                )

        if current is not None:
            networks.append(current)

        return networks

    except subprocess.TimeoutExpired:
        raise RuntimeError("Wi-Fi scan timed out. Try again.")

    except OSError as error:
        raise RuntimeError(
            f"Unable to run Windows Wi-Fi scan: {error}"
        )
