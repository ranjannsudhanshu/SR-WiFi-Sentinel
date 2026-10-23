
import csv
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "history.csv"

FIELDS = [
    "timestamp",
    "ssid",
    "signal",
    "authentication",
    "encryption",
    "risk",
    "findings",
]


def save_scan_history(networks):
    """Append the latest scan results to CSV history."""

    from security_check import assess_network

    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    file_exists = (
        HISTORY_FILE.exists()
        and HISTORY_FILE.stat().st_size > 0
    )

    with HISTORY_FILE.open(
        "a",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
        )

        if not file_exists:
            writer.writeheader()

        for network in networks:
            report = assess_network(network)

            writer.writerow({
                "timestamp": timestamp,
                "ssid": network.get("ssid", ""),
                "signal": network.get("signal", ""),
                "authentication": network.get(
                    "authentication", "Unknown"
                ),
                "encryption": network.get(
                    "encryption", "Unknown"
                ),
                "risk": report["risk"],
                "findings": " | ".join(
                    report["findings"]
                ),
            })

    return HISTORY_FILE


def export_scan(networks, destination):
    """Export current scan results to a CSV chosen by user."""

    import csv
    from security_check import assess_network

    with open(
        destination,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
        )
        writer.writeheader()

        timestamp = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )

        for network in networks:
            report = assess_network(network)

            writer.writerow({
                "timestamp": timestamp,
                "ssid": network.get("ssid", ""),
                "signal": network.get("signal", ""),
                "authentication": network.get(
                    "authentication", "Unknown"
                ),
                "encryption": network.get(
                    "encryption", "Unknown"
                ),
                "risk": report["risk"],
                "findings": " | ".join(
                    report["findings"]
                ),
            })
