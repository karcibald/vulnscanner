
# 🔍 Lightweight Vulnerability Scanner Dashboard (AWS + Flask)

A cloud-hosted vulnerability management system that:
- Scans targets using Nmap
- Logs results to DynamoDB
- Sends SNS email alerts for risky open ports (22, 3389, etc.)
- Displays results via a Flask dashboard
- Performs GeoIP lookups for host info

## 🔧 Stack
- AWS EC2 (Ubuntu)
- Python 3 + Flask + Boto3
- Nmap (via python-nmap)
- DynamoDB
- AWS SNS (for alerting)

## ✅ Features
- 🔐 IAM Role + Metadata access (no hardcoded keys)
- 🛡️ Port status detection (open / closed / filtered)
- 📬 Email alerts via SNS
- 📊 Web dashboard with GeoIP, filtering & sorting
- 🗺️ Country flag + ISP + region + city

## 🖼️ Lab Output Evidence

![Lab Screenshot](vulnscan_lab_evidence.jpg)

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install flask boto3 python-nmap requests

# 2. Start the scanner
python3 scanner.py

# 3. Run the Flask web dashboard
python3 app.py
```

Access the dashboard at:
```
http://<your-ec2-ip>:5000
```

## 📁 Structure

```
vulnscanner-dashboard/
├── scanner.py
├── app.py
├── templates/
│   └── index.html
├── README.md
└── vulnscan_lab_evidence.jpg
```

## 💡 Future Ideas

- Export scan logs to CSV
- Real-time auto-refresh dashboard
- Slack/Discord webhook alerts
- Host tagging / grouping
