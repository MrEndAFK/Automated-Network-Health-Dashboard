from flask import Flask, jsonify, render_template
from ping3 import ping
import psutil

app = Flask(__name__)

# Define the servers to monitor
# Update the servers you want to check here:)
############################
server1 = "8.8.8.8"
server2 = "1.1.1.1"
server3 = "example.com"
############################
servers = [ server1, server2, server3 ]

def check_latency():
    results = {}
    for server in servers:
        try:
            latency = ping(server, timeout=2)
            results[server] = round(latency * 1000, 2) if latency else None
        except Exception as e:
            results[server] = None
    return results

def monitor_bandwidth():
    net_stats = psutil.net_io_counters()
    return {
        "bytes_sent": net_stats.bytes_sent,
        "bytes_recv": net_stats.bytes_recv,
    }

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/api/latencies")
def get_latencies():
    latencies = check_latency()
    return jsonify(latencies)

@app.route("/api/bandwidth")
def get_bandwidth():
    bandwidth = monitor_bandwidth()
    return jsonify(bandwidth)

if __name__ == "__main__":
    app.run(debug=True)
