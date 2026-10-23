
def assess_network(network):
    """Assess visible Wi-Fi security indicators."""

    authentication = network.get("authentication", "").strip().lower()
    encryption = network.get("encryption", "").strip().lower()

    findings = []

    if authentication in ("open", "none") or encryption in ("none", "open"):
        risk = "HIGH"
        findings.append(
            "No Wi-Fi encryption detected. Traffic may be exposed."
        )

    elif "wep" in authentication or "wep" in encryption:
        risk = "HIGH"
        findings.append(
            "WEP is obsolete and insecure."
        )

    elif "wpa3" in authentication:
        risk = "LOW"
        findings.append(
            "WPA3 authentication detected; this is a positive indicator."
        )

    elif "wpa2" in authentication:
        risk = "LOW"
        findings.append(
            "WPA2 authentication detected; keep router firmware updated."
        )

    elif "wpa" in authentication:
        risk = "MEDIUM"
        findings.append(
            "Legacy WPA detected. Prefer WPA2-AES or WPA3."
        )

    else:
        risk = "UNKNOWN"
        findings.append(
            "Authentication could not be classified reliably."
        )

    return {
        "risk": risk,
        "findings": findings,
    }


def display_risk_report(networks):
    if not networks:
        print("No networks available for security assessment.")
        return

    print("\n======= SR WIFI SENTINEL: RISK REPORT =======")

    for network in networks:
        report = assess_network(network)

        print(f"\nNetwork: {network.get('ssid', 'Unknown')}")
        print(f"Risk level: {report['risk']}")

        for finding in report["findings"]:
            print(f" - {finding}")

        print("-" * 45)

def assess_network(network):
    """Classify visible Wi-Fi security indicators."""

    authentication = (
        network.get("authentication", "")
        .strip()
        .lower()
    )
    encryption = (
        network.get("encryption", "")
        .strip()
        .lower()
    )

    findings = []

    if (
        "wep" in authentication
        or "wep" in encryption
    ):
        risk = "HIGH"
        findings.append(
            "WEP is obsolete and insecure."
        )

    elif (
        authentication in ("open", "none")
        or encryption in ("none", "open")
    ):
        risk = "HIGH"
        findings.append(
            "No Wi-Fi encryption detected."
        )

    elif "wpa3" in authentication:
        risk = "LOW"
        findings.append(
            "WPA3 authentication detected. "
            "This is a positive security indicator."
        )

    elif "wpa2" in authentication:
        risk = "LOW"
        findings.append(
            "WPA2 authentication detected. "
            "Keep router firmware updated."
        )

    elif authentication == "wpa":
        risk = "MEDIUM"
        findings.append(
            "Legacy WPA detected. Prefer WPA2-AES or WPA3."
        )

    else:
        risk = "UNKNOWN"
        findings.append(
            "Security could not be classified reliably."
        )

    return {
        "risk": risk,
        "findings": findings,
    }


def display_risk_report(networks):
    print("\n======= SR WIFI SENTINEL: RISK REPORT =======")

    for network in networks:
        report = assess_network(network)

        print(f"\nNetwork: {network['ssid']}")
        print(f"Risk level: {report['risk']}")

        for finding in report["findings"]:
            print(f" - {finding}")

        print("-" * 45)
