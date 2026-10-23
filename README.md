# 🛡️ SR-WiFi-Sentinel

### Wi-Fi Security Scanner & Risk Monitoring Dashboard

**Developed by SR CyberLabs | Sudhanshu Ranjan**

SR-WiFi-Sentinel is a Python-based Windows desktop application designed to inspect nearby Wi-Fi networks and highlight potential security risks. It helps users understand visible network security indicators before deciding whether to connect.

The project combines Wi-Fi scanning, risk classification, security explanations, alerts, and scan history in one desktop dashboard.

> **Disclaimer:** A security warning indicates potential risk, not proof that a network is malicious. The application does not automatically connect to, block, or disconnect from any Wi-Fi network.

---

## ✨ Features

- **📡 Wi-Fi Network Scanner** — View available wireless networks and their reported security information.
- **🔎 Security Risk Analysis** — Identify indicators such as open networks or weak/missing encryption where reported by the system.
- **🚨 Risk Alerts** — Display warnings and explanations to help users assess potential risks.
- **📊 Desktop Dashboard** — Access scanning and monitoring features through a graphical interface.
- **🗂️ Scan History** — Review recorded scan results using the project's history feature.
- **🛡️ User-Controlled Decisions** — Users decide whether to connect or disconnect; the tool does not automatically change Wi-Fi connections.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Tkinter / GUI modules | Desktop interface |
| Windows WLAN tools | Retrieve available Wi-Fi information |
| CSV / Python file handling | Scan history, depending on configuration |

## 📁 Project Structure

```text
SR-WiFi-Sentinel/
├── main.py
├── gui.py
├── scanner.py
├── security_check.py
├── alerts.py
├── history.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Requirements

- Windows 10 or Windows 11
- Python installed on the system
- Wi-Fi adapter enabled
- VS Code or another Python editor (optional)

Some wireless information may depend on Windows permissions, WLAN driver support, and system settings.

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/ranjannsudhanshu/SR-WiFi-Sentinel.git
```

### 2. Open the project folder

```bash
cd SR-WiFi-Sentinel
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

**Command Prompt:**

```cmd
.venv\Scripts\activate
```

**PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

Start with the project's main entry point:

```bash
python main.py
```

If your local project uses a different startup file, use the entry point configured in that version.

## 🖥️ How to Use

1. Launch the desktop application.
2. Open the Wi-Fi scanner or dashboard section.
3. Run a scan to retrieve available wireless network information.
4. Review the security indicators, risk classification, and explanations shown by the application.
5. Check scan history if the feature is enabled.
6. Make your own informed decision about connecting to a network.

## 🔐 Privacy & Safety

- The tool is intended for local Wi-Fi security awareness.
- A scan does not prove that a network is safe or malicious.
- Risk results depend on the information available from Windows and the wireless adapter.
- The application does not automatically block networks or disconnect users.
- Review the code and configuration before using the project in a sensitive environment.

## 🎯 Project Goal

The goal of SR-WiFi-Sentinel is to make basic Wi-Fi security indicators easier to understand through a simple desktop interface. It is an educational cybersecurity project intended to support awareness, not replace professional security testing.

## 🔮 Future Improvements

- More detailed scan reports
- Exportable scan history
- Improved risk explanations
- Additional dashboard visualizations
- Automated tests and expanded documentation

## 👨‍💻 Author

**Sudhanshu Ranjan**  
Project brand: **SR CyberLabs**

- GitHub: [@ranjannsudhanshu](https://github.com/ranjannsudhanshu)
- Project repository: [SR-WiFi-Sentinel](https://github.com/ranjannsudhanshu/SR-WiFi-Sentinel)

---

*Built for learning, experimentation, and Wi-Fi security awareness.*
