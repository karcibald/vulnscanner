
from flask import Flask, render_template
import boto3
import requests

app = Flask(__name__)

def get_geoip(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=2).json()
        if res["status"] == "success":
            return {
                "country": res.get("country", ""),
                "city": res.get("city", ""),
                "region": res.get("regionName", ""),
                "isp": res.get("isp", ""),
                "emoji": country_flag(res.get("countryCode", ""))
            }
    except:
        pass
    return {"country": "", "city": "", "region": "", "isp": "", "emoji": ""}

def country_flag(code):
    return ''.join(chr(127397 + ord(c)) for c in code.upper()) if code else ''

@app.route('/')
def index():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('VulnScanResults')
    response = table.scan()
    items = response['Items']
    for item in items:
        ip = item["Host"]
        geo = get_geoip(ip)
        item["Country"] = geo["emoji"] + " " + geo["country"]
        item["City"] = geo["city"]
        item["Region"] = geo["region"]
        item["ISP"] = geo["isp"]
    items = sorted(items, key=lambda x: x['Timestamp'], reverse=True)
    return render_template('index.html', scans=items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
