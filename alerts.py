
from security_check import assess_network


def show_security_alerts(networks):
    print("\n" + "=" * 48)
    print("        SR WIFI SENTINEL - ALERTS")
    print("=" * 48)

    if not networks:
        print("No scan data available.")
        return

    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
    alerts = []

    for network in networks:
        report = assess_network(network)
        risk = report["risk"]

        counts[risk] = counts.get(risk, 0) + 1

        if risk in ("HIGH", "MEDIUM"):
            alerts.append((network, report))

    print(f"\nNetworks scanned : {len(networks)}")
    print(f"HIGH risk        : {counts['HIGH']}")
    print(f"MEDIUM risk      : {counts['MEDIUM']}")
    print(f"LOW risk         : {counts['LOW']}")
    print(f"UNKNOWN          : {counts['UNKNOWN']}")

    if alerts:
        print("\n[SECURITY ALERTS]")

        for network, report in alerts:
            print(f"\nNetwork: {network.get('ssid', 'Unknown')}")
            print(f"Risk level: {report['risk']}")

            for finding in report["findings"]:
                print(f"Reason: {finding}")

            print("Advice: Verify the network before connecting.")
    else:
        print("\nNo HIGH or MEDIUM indicators detected.")

    print("\nRisk indicators do not prove a network is malicious.")
    print("=" * 48)
