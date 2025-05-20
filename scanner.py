
import nmap
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('VulnScanResults')
sns = boto3.client('sns', region_name='us-east-1')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:VulnAlerts'

targets = ['scanme.nmap.org', 'testphp.vulnweb.com', 'httpbin.org', '192.168.0.1']
scan_ports = '22,80,443,3389'
risky_ports = [22, 3389]

nm = nmap.PortScanner()

for target in targets:
    print(f"[*] Scanning {target}...")
    try:
        nm.scan(target, arguments=f'-Pn -T4 -p {scan_ports}')
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                for port in nm[host][proto].keys():
                    state = nm[host][proto][port]['state']
                    timestamp = datetime.now(timezone.utc).isoformat()
                    result = {
                        'ScanID': f"{host}_{port}_{int(datetime.now(timezone.utc).timestamp())}",
                        'Host': host,
                        'Port': int(port),
                        'State': state,
                        'Timestamp': timestamp
                    }
                    table.put_item(Item=result)
                    print(f"[+] Logged: {host}:{port} → {state}")
                    if port in risky_ports and state == 'open':
                        msg = f"⚠️ Vulnerability Alert!\n\nTarget: {host}\nPort: {port} is OPEN\nTime: {timestamp}"
                        sns.publish(TopicArn=SNS_TOPIC_ARN, Subject="⚠️ Open Port Detected", Message=msg)
                        print(f"[ALERT] Sent SNS notification for {host}:{port}")
    except Exception as e:
        print(f"[!] Failed to scan {target}: {e}")
