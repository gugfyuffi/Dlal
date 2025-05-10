
from flask import Flask, request
from datetime import datetime
import json
import requests

app = Flask(__name__)
log_file = "visitors.log"

@app.route("/ping", methods=["POST"])
def ping():
    data = request.get_json()
    ip = request.remote_addr
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        lat = geo.get('lat')
        lon = geo.get('lon')
        location = f"{geo.get('country')}, {geo.get('regionName')} - {geo.get('city')} (lat: {lat}, lon: {lon})"
        map_link = f"https://www.google.com/maps?q={lat},{lon}"
    except:
        location = "Unknown"
        map_link = "Unavailable"

    with open(log_file, "a") as f:
        f.write(f"[PING] {now} - IP: {ip} - LOCATION: {location} - {json.dumps(data)}\n")
        f.write(f"[MAP] {map_link}\n{'-'*40}\n")

    return "OK"

@app.route("/")
def home():
    return open("index.html").read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
