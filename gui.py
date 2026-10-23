
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from scanner import scan_wifi_networks
from security_check import assess_network
from history import save_scan_history, export_scan


# ==================== COLORS ====================
BG = "#000000"
SIDEBAR = "#050505"
CARD = "#0D0D0D"
CARD_HOVER = "#1A1A1A"

BLUE = "#1677FF"
CYAN = "#00D9FF"
GREEN = "#22C993"
ORANGE = "#FFAA45"
RED = "#FF5C75"
HEART_RED = "#FF3030"

WHITE = "#FFFFFF"
MUTED = "#A0A0A0"
BORDER = "#252525"


class WiFiSentinelApp:

    def __init__(self, root):
        self.root = root
        self.root.title("SR WiFi Sentinel")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 680)
        self.root.configure(bg=BG)

        self.networks = []
        self.scanning = False
        self.sidebar_items = {}
        self.active_section = "Dashboard"

        self.setup_styles()
        self.build_dashboard()

    # ==================== STYLES ====================
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Sentinel.Treeview",
            background=CARD,
            foreground=WHITE,
            fieldbackground=CARD,
            borderwidth=0,
            rowheight=42,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Sentinel.Treeview.Heading",
            background="#171717",
            foreground=CYAN,
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padding=(10, 14)
        )

        style.map(
            "Sentinel.Treeview",
            background=[("selected", "#12385C")],
            foreground=[("selected", WHITE)]
        )

        style.map(
            "Sentinel.Treeview.Heading",
            background=[("active", "#252525")]
        )

        style.configure(
            "Sentinel.Vertical.TScrollbar",
            background="#252525",
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=CYAN
        )

    # ==================== UI HELPERS ====================
    def make_label(
        self, parent, text, size=10, color=WHITE, bold=False, **kwargs
    ):
        font_weight = "bold" if bold else "normal"

        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", size, font_weight),
            bg=kwargs.pop("bg", parent.cget("bg")),
            fg=color,
            **kwargs
        )

    def make_button(
        self, parent, text, command, color=BLUE, fg=WHITE, width=None
    ):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=fg,
            activebackground=CARD_HOVER,
            activeforeground=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=16,
            pady=11,
            width=width
        )

        button.bind(
            "<Enter>",
            lambda event: button.configure(bg=CARD_HOVER)
            if button["state"] != "disabled" else None
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(bg=color)
            if button["state"] != "disabled" else None
        )

        return button

    def make_card(self, parent):
        return tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            bd=0
        )

    # ==================== DASHBOARD LAYOUT ====================
    def build_dashboard(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # LEFT SIDEBAR
        sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=235
        )
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        # LOGO
        logo_area = tk.Frame(sidebar, bg=SIDEBAR)
        logo_area.pack(
            fill="x",
            padx=22,
            pady=(28, 26)
        )

        tk.Label(
            logo_area,
            text="SR",
            font=("Segoe UI", 20, "bold"),
            bg=BLUE,
            fg=WHITE,
            width=3,
            pady=8
        ).pack(anchor="w", pady=(0, 14))

        self.make_label(
            logo_area,
            "WIFI SENTINEL",
            15,
            WHITE,
            True
        ).pack(anchor="w")

        self.make_label(
            logo_area,
            "NETWORK SECURITY",
            8,
            CYAN,
            True
        ).pack(anchor="w", pady=(5, 0))

        tk.Frame(
            sidebar,
            bg=BORDER,
            height=1
        ).pack(fill="x", padx=18, pady=(0, 22))

        self.make_label(
            sidebar,
            "WORKSPACE",
            9,
            MUTED,
            True
        ).pack(anchor="w", padx=22, pady=(0, 12))

        # SIDEBAR NAVIGATION
        self.make_sidebar_item(
            sidebar,
            "▦   Dashboard",
            "Dashboard",
            lambda: self.show_section("Dashboard")
        )

        self.make_sidebar_item(
            sidebar,
            "⌁   Wi-Fi Scanner",
            "Wi-Fi Scanner",
            self.start_scan
        )

        self.make_sidebar_item(
            sidebar,
            "◉   Risk Monitoring",
            "Risk Monitoring",
            lambda: self.show_section("Risk Monitoring")
        )

        self.make_sidebar_item(
            sidebar,
            "▤   Scan History",
            "Scan History",
            self.open_history
        )

        # FLEXIBLE SPACE
        tk.Frame(
            sidebar,
            bg=SIDEBAR
        ).pack(fill="both", expand=True)

        # SYSTEM STATUS CARD
        security_box = tk.Frame(
            sidebar,
            bg="#0B1714",
            highlightbackground="#174438",
            highlightthickness=1
        )
        security_box.pack(
            fill="x",
            padx=14,
            pady=(12, 15)
        )

        self.make_label(
            security_box,
            "●  SYSTEM STATUS",
            9,
            GREEN,
            True
        ).pack(anchor="w", padx=13, pady=(13, 6))

        self.system_status = self.make_label(
            security_box,
            "Ready to scan",
            10,
            WHITE
        )
        self.system_status.pack(
            anchor="w",
            padx=13,
            pady=(0, 13)
        )

        # CENTERED BRANDING FOOTER
        footer_brand = tk.Frame(
            sidebar,
            bg=SIDEBAR
        )
        footer_brand.pack(
            side="bottom",
            fill="x",
            padx=8,
            pady=(0, 20)
        )

        tk.Frame(
            footer_brand,
            bg=BORDER,
            height=1
        ).pack(
            fill="x",
            padx=12,
            pady=(0, 14)
        )

        # Separate labels allow the heart to be red.
        brand_text = tk.Frame(
            footer_brand,
            bg=SIDEBAR
        )
        brand_text.pack(anchor="center")

        tk.Label(
            brand_text,
            text="Made with",
            font=("Segoe UI", 9, "bold"),
            bg=SIDEBAR,
            fg=CYAN
        ).pack(side="left")

        tk.Label(
            brand_text,
            text=" ♥ ",
            font=("Segoe UI", 10, "bold"),
            bg=SIDEBAR,
            fg=HEART_RED
        ).pack(side="left")

        tk.Label(
            brand_text,
            text="by SR CyberLabs",
            font=("Segoe UI", 9, "bold"),
            bg=SIDEBAR,
            fg=CYAN
        ).pack(side="left")

        # MAIN CONTENT
        main = tk.Frame(
            self.root,
            bg=BG
        )
        main.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=30,
            pady=26
        )

        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(3, weight=1)

        # HEADER
        header = tk.Frame(main, bg=BG)
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 24)
        )
        header.grid_columnconfigure(0, weight=1)

        heading = tk.Frame(header, bg=BG)
        heading.grid(row=0, column=0, sticky="w")

        self.page_title = self.make_label(
            heading,
            "Network Security Dashboard",
            23,
            WHITE,
            True
        )
        self.page_title.pack(anchor="w")

        self.page_subtitle = self.make_label(
            heading,
            "Monitor nearby Wi-Fi networks and review security risks.",
            10,
            MUTED
        )
        self.page_subtitle.pack(anchor="w", pady=(7, 0))

        self.scan_button = self.make_button(
            header,
            "⟳   Scan Wi-Fi",
            self.start_scan,
            BLUE
        )
        self.scan_button.grid(
            row=0,
            column=1,
            padx=(14, 0),
            sticky="e"
        )

        # SUMMARY CARDS
        stats = tk.Frame(main, bg=BG)
        stats.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 20)
        )

        for i in range(4):
            stats.grid_columnconfigure(
                i,
                weight=1,
                uniform="stats"
            )

        self.total_value = self.make_stat_card(
            stats, 0, "NETWORKS FOUND",
            "0", CYAN, "Nearby networks"
        )

        self.high_value = self.make_stat_card(
            stats, 1, "HIGH RISK",
            "0", RED, "Needs attention"
        )

        self.medium_value = self.make_stat_card(
            stats, 2, "MEDIUM RISK",
            "0", ORANGE, "Review security"
        )

        self.low_value = self.make_stat_card(
            stats, 3, "LOW RISK",
            "0", GREEN, "Stronger settings"
        )

        # SCAN STATUS
        status_card = self.make_card(main)
        status_card.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 20)
        )
        status_card.grid_columnconfigure(0, weight=1)

        status_left = tk.Frame(status_card, bg=CARD)
        status_left.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=15
        )

        self.make_label(
            status_left,
            "●  LIVE SCAN STATUS",
            9,
            CYAN,
            True
        ).pack(anchor="w")

        self.status_text = self.make_label(
            status_left,
            "Ready. Click Scan Wi-Fi to begin.",
            10,
            WHITE
        )
        self.status_text.pack(anchor="w", pady=(6, 0))

        self.last_scan_label = self.make_label(
            status_card,
            "Last scan: Not yet scanned",
            9,
            MUTED
        )
        self.last_scan_label.grid(
            row=0,
            column=1,
            padx=18,
            pady=15,
            sticky="e"
        )

        # NETWORK TABLE
        table_card = self.make_card(main)
        table_card.grid(
            row=3,
            column=0,
            sticky="nsew"
        )
        table_card.grid_rowconfigure(1, weight=1)
        table_card.grid_columnconfigure(0, weight=1)

        table_header = tk.Frame(table_card, bg=CARD)
        table_header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=16
        )
        table_header.grid_columnconfigure(0, weight=1)

        self.make_label(
            table_header,
            "Detected Wi-Fi Networks",
            13,
            WHITE,
            True
        ).grid(row=0, column=0, sticky="w")

        self.make_label(
            table_header,
            "SECURITY OVERVIEW",
            8,
            MUTED,
            True
        ).grid(row=0, column=1, sticky="e")

        table_area = tk.Frame(table_card, bg=CARD)
        table_area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(0, 12)
        )
        table_area.grid_rowconfigure(0, weight=1)
        table_area.grid_columnconfigure(0, weight=1)

        columns = (
            "ssid",
            "signal",
            "authentication",
            "encryption",
            "risk"
        )

        self.table = ttk.Treeview(
            table_area,
            columns=columns,
            show="headings",
            style="Sentinel.Treeview"
        )

        self.table.heading("ssid", text="NETWORK NAME")
        self.table.heading("signal", text="SIGNAL")
        self.table.heading("authentication", text="AUTHENTICATION")
        self.table.heading("encryption", text="ENCRYPTION")
        self.table.heading("risk", text="RISK LEVEL")

        self.table.column("ssid", width=220, minwidth=120)
        self.table.column("signal", width=90, anchor="center")
        self.table.column("authentication", width=170)
        self.table.column("encryption", width=140)
        self.table.column("risk", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_area,
            orient="vertical",
            command=self.table.yview,
            style="Sentinel.Vertical.TScrollbar"
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.table.tag_configure("HIGH", foreground=RED)
        self.table.tag_configure("MEDIUM", foreground=ORANGE)
        self.table.tag_configure("LOW", foreground=GREEN)
        self.table.tag_configure("UNKNOWN", foreground=MUTED)

        # FOOTER ACTIONS
        footer = tk.Frame(main, bg=BG)
        footer.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(16, 0)
        )

        self.make_button(
            footer,
            "↓  Export CSV",
            self.export_current,
            "#171717"
        ).pack(side="left")

        self.make_button(
            footer,
            "▤  Open Scan History",
            self.open_history,
            "#171717"
        ).pack(side="left", padx=10)

        self.make_label(
            footer,
            "All Clear",
            9,
            MUTED
        ).pack(side="right", pady=10)

    # ==================== SIDEBAR NAVIGATION ====================
    def make_sidebar_item(
        self, parent, text, section, command
    ):
        selected = section == self.active_section

        item = tk.Label(
            parent,
            text=text,
            font=(
                "Segoe UI",
                10,
                "bold" if selected else "normal"
            ),
            bg="#123052" if selected else SIDEBAR,
            fg=CYAN if selected else MUTED,
            anchor="w",
            padx=18,
            pady=13,
            cursor="hand2"
        )
        item.pack(fill="x", padx=10, pady=3)

        self.sidebar_items[section] = item

        item.bind(
            "<Button-1>",
            lambda event: command()
        )

        item.bind(
            "<Enter>",
            lambda event: item.configure(
                bg="#123052",
                fg=CYAN
            )
        )

        item.bind(
            "<Leave>",
            lambda event: self.reset_sidebar_item(section)
        )

    def reset_sidebar_item(self, section):
        item = self.sidebar_items.get(section)

        if item is None:
            return

        selected = self.active_section == section

        item.configure(
            bg="#123052" if selected else SIDEBAR,
            fg=CYAN if selected else MUTED,
            font=(
                "Segoe UI",
                10,
                "bold" if selected else "normal"
            )
        )

    def select_sidebar_item(self, section):
        self.active_section = section

        for name in self.sidebar_items:
            self.reset_sidebar_item(name)

    # ==================== STAT CARDS ====================
    def make_stat_card(
        self, parent, column, title, value, color, caption
    ):
        card = self.make_card(parent)

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(
                0 if column == 0 else 7,
                7 if column < 3 else 0
            )
        )

        tk.Frame(
            card,
            bg=color,
            height=3
        ).pack(fill="x")

        content = tk.Frame(card, bg=CARD)
        content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.make_label(
            content,
            title,
            8,
            MUTED,
            True
        ).pack(anchor="w")

        value_label = self.make_label(
            content,
            value,
            27,
            color,
            True
        )
        value_label.pack(anchor="w", pady=(7, 2))

        self.make_label(
            content,
            caption,
            8,
            MUTED
        ).pack(anchor="w")

        return value_label

    # ==================== NAVIGATION ====================
    def show_section(self, section):
        self.select_sidebar_item(section)

        if section == "Dashboard":
            self.page_title.configure(
                text="Network Security Dashboard"
            )
            self.page_subtitle.configure(
                text=(
                    "Monitor nearby Wi-Fi networks and "
                    "review security risks."
                )
            )

            self.status_text.configure(
                text="Dashboard selected. Ready to monitor Wi-Fi.",
                fg=CYAN
            )

        elif section == "Risk Monitoring":
            self.page_title.configure(
                text="Risk Monitoring"
            )
            self.page_subtitle.configure(
                text="Review security assessments for the latest scan."
            )

            if not self.networks:
                self.status_text.configure(
                    text="No scan data available. Scan Wi-Fi first.",
                    fg=ORANGE
                )

                messagebox.showinfo(
                    "Risk Monitoring",
                    "Please scan Wi-Fi networks first."
                )
                return

            counts = {
                "HIGH": 0,
                "MEDIUM": 0,
                "LOW": 0,
                "UNKNOWN": 0
            }

            for network in self.networks:
                risk = self.get_risk(network)
                counts[risk] += 1

            self.status_text.configure(
                text=(
                    f"Risk summary: {counts['HIGH']} HIGH  |  "
                    f"{counts['MEDIUM']} MEDIUM  |  "
                    f"{counts['LOW']} LOW  |  "
                    f"{counts['UNKNOWN']} UNKNOWN"
                ),
                fg=RED if counts["HIGH"] else GREEN
            )

            messagebox.showinfo(
                "Risk Monitoring Summary",
                f"Networks scanned: {len(self.networks)}\n\n"
                f"HIGH risk: {counts['HIGH']}\n"
                f"MEDIUM risk: {counts['MEDIUM']}\n"
                f"LOW risk: {counts['LOW']}\n"
                f"UNKNOWN: {counts['UNKNOWN']}\n\n"
                "Risk labels describe observed security settings; "
                "they do not prove a network is malicious."
            )

    # ==================== SCANNING ====================
    def start_scan(self):
        if self.scanning:
            return

        self.select_sidebar_item("Wi-Fi Scanner")

        self.page_title.configure(text="Wi-Fi Scanner")
        self.page_subtitle.configure(
            text=(
                "Discover nearby Wi-Fi networks and "
                "review their settings."
            )
        )

        self.scanning = True

        self.scan_button.configure(
            text="Scanning...",
            state="disabled",
            bg="#202020"
        )

        self.system_status.configure(text="Scanning...")

        self.status_text.configure(
            text="Scanning nearby Wi-Fi networks...",
            fg=CYAN
        )

        threading.Thread(
            target=self.scan_worker,
            daemon=True
        ).start()

    def scan_worker(self):
        try:
            networks = scan_wifi_networks()

            self.root.after(
                0,
                lambda: self.show_results(networks)
            )

        except Exception as exc:
            error_text = str(exc)

            self.root.after(
                0,
                lambda: self.show_scan_error(error_text)
            )

    def get_network_value(
        self, network, *keys, default="Unknown"
    ):
        for key in keys:
            if key in network and network[key] is not None:
                return network[key]

        return default

    def get_risk(self, network):
        try:
            result = assess_network(network)

            if isinstance(result, dict):
                risk = result.get(
                    "risk",
                    result.get("level", "UNKNOWN")
                )

            elif isinstance(result, (tuple, list)):
                risk = result[0] if result else "UNKNOWN"

            else:
                risk = result

            risk = str(risk).upper()

            if "HIGH" in risk:
                return "HIGH"

            if "MEDIUM" in risk:
                return "MEDIUM"

            if "LOW" in risk:
                return "LOW"

            return "UNKNOWN"

        except Exception:
            return "UNKNOWN"

    def show_results(self, networks):
        self.scanning = False

        self.scan_button.configure(
            text="⟳   Scan Wi-Fi",
            state="normal",
            bg=BLUE
        )

        self.system_status.configure(
            text="Scan complete"
        )

        self.networks = networks

        for item in self.table.get_children():
            self.table.delete(item)

        counts = {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "UNKNOWN": 0
        }

        for network in networks:
            ssid = self.get_network_value(
                network, "ssid", "SSID"
            )

            signal = self.get_network_value(
                network, "signal", "Signal", "signal_strength"
            )

            auth = self.get_network_value(
                network, "authentication",
                "Authentication", "auth"
            )

            encryption = self.get_network_value(
                network, "encryption", "Encryption"
            )

            risk = self.get_risk(network)
            counts[risk] += 1

            signal_text = str(signal)

            if signal_text.isdigit():
                signal_text += "%"

            self.table.insert(
                "",
                "end",
                values=(
                    ssid,
                    signal_text,
                    auth,
                    encryption,
                    risk
                ),
                tags=(risk,)
            )

        self.total_value.configure(
            text=str(len(networks))
        )

        self.high_value.configure(
            text=str(counts["HIGH"])
        )

        self.medium_value.configure(
            text=str(counts["MEDIUM"])
        )

        self.low_value.configure(
            text=str(counts["LOW"])
        )

        now = datetime.now().strftime(
            "%d %b %Y, %I:%M %p"
        )

        self.last_scan_label.configure(
            text=f"Last scan: {now}"
        )

        self.status_text.configure(
            text=(
                f"Scan complete — {len(networks)} "
                "network(s) detected."
            ),
            fg=GREEN
        )

        try:
            save_scan_history(networks)

        except Exception as exc:
            messagebox.showwarning(
                "History Warning",
                "Scan completed, but history could not be saved:\n"
                f"{exc}"
            )

        if counts["HIGH"] > 0:
            messagebox.showwarning(
                "Security Alert",
                f"{counts['HIGH']} network(s) were flagged as HIGH risk.\n\n"
                "Review their security settings before connecting. "
                "This does not prove a network is malicious."
            )

        elif counts["MEDIUM"] > 0:
            messagebox.showinfo(
                "Scan Complete",
                "Some networks use older or less preferred security "
                "settings. Review the table before connecting."
            )

    def show_scan_error(self, error_text):
        self.scanning = False

        self.scan_button.configure(
            text="⟳   Scan Wi-Fi",
            state="normal",
            bg=BLUE
        )

        self.system_status.configure(
            text="Scan failed"
        )

        self.status_text.configure(
            text="Scan failed. Check permissions and try again.",
            fg=RED
        )

        messagebox.showerror(
            "Wi-Fi Scan Error",
            f"Could not scan Wi-Fi networks.\n\n"
            f"{error_text}\n\n"
            "Check that Wi-Fi is enabled and Windows Location "
            "permission is available if required."
        )

    # ==================== CSV EXPORT ====================
    def export_current(self):
        if not self.networks:
            messagebox.showinfo(
                "No Scan Data",
                "Scan Wi-Fi networks first, then export the results."
            )
            return

        destination = filedialog.asksaveasfilename(
            title="Export Wi-Fi Scan",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="sr_wifi_scan.csv"
        )

        if not destination:
            return

        try:
            export_scan(self.networks, destination)

            messagebox.showinfo(
                "Export Complete",
                "Scan results exported successfully:\n"
                f"{destination}"
            )

        except Exception as exc:
            messagebox.showerror(
                "Export Failed",
                str(exc)
            )

    # ==================== SCAN HISTORY ====================
    def open_history(self):
        self.select_sidebar_item("Scan History")

        self.page_title.configure(
            text="Scan History"
        )

        self.page_subtitle.configure(
            text="Open the CSV file containing your saved scan history."
        )

        history_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "history.csv"
        )

        if not os.path.exists(history_path):
            self.status_text.configure(
                text="No saved scan history found yet.",
                fg=ORANGE
            )

            messagebox.showinfo(
                "No History Yet",
                "Your scan history will appear here after your first scan."
            )
            return

        try:
            os.startfile(history_path)

            self.status_text.configure(
                text="Scan history opened successfully.",
                fg=GREEN
            )

        except Exception as exc:
            messagebox.showerror(
                "Could Not Open History",
                str(exc)
            )


def main():
    root = tk.Tk()
    WiFiSentinelApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
