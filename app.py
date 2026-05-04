from flask import Flask, jsonify, render_template, request
import csv
import os
from data_generator import generate_traffic_data

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.csv")

PORT_MAP = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    135: "RPC",
    143: "IMAP",
    161: "SNMP",
    443: "HTTPS",
    445: "SMB",
    500: "IKE",
    587: "SMTP-TLS",
    993: "IMAPS",
    3306: "MySQL",
    3389: "RDP",
    5353: "mDNS",
    8080: "HTTP-Alt",
    1900: "SSDP",
    4500: "IPSec",
}

monitoring_active = False
generated_count = 0


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def get_service(port):
    port = to_int(port)
    return "ICMP" if port == 0 else PORT_MAP.get(port, "Unknown")


def load_all_records():
    if not os.path.exists(DATA_FILE):
        return []

    records = []
    with open(DATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            packet = {
                "time": row.get("time", ""),
                "source_ip": row.get("source_ip", ""),
                "destination_ip": row.get("destination_ip", ""),
                "protocol": row.get("protocol", ""),
                "port": to_int(row.get("port")),
                "packet_size": to_int(row.get("packet_size")),
            }
            packet["service"] = get_service(packet["port"])
            records.append(packet)
    return records


def filter_records(records, protocol, source_ip, dest_ip):
    protocol = protocol.strip().upper()
    source_ip = source_ip.strip().lower()
    dest_ip = dest_ip.strip().lower()

    filtered = []
    for record in records:
        if protocol and record["protocol"].upper() != protocol:
            continue
        if source_ip and source_ip not in record["source_ip"].lower():
            continue
        if dest_ip and dest_ip not in record["destination_ip"].lower():
            continue
        filtered.append(record)
    return filtered


def compute_stats(records):
    total = len(records)
    counts = {"TCP": 0, "UDP": 0, "ICMP": 0}
    size_sum = 0

    for record in records:
        protocol = record.get("protocol", "").upper()
        if protocol in counts:
            counts[protocol] += 1
        size_sum += to_int(record.get("packet_size"))

    avg_size = round(size_sum / total, 2) if total else 0
    return {
        "total_packets": total,
        "tcp_count": counts["TCP"],
        "udp_count": counts["UDP"],
        "icmp_count": counts["ICMP"],
        "avg_packet_size": avg_size,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_monitoring():
    global monitoring_active
    monitoring_active = True
    return jsonify({"status": "started"})


@app.route("/stop", methods=["POST"])
def stop_monitoring():
    global monitoring_active
    monitoring_active = False
    return jsonify({"status": "stopped"})


@app.route("/data", methods=["GET"])
def get_data():
    protocol  = request.args.get("protocol",  "").strip()
    source_ip = request.args.get("source_ip", "").strip()
    dest_ip   = request.args.get("dest_ip",   "").strip()

    all_records = load_all_records()
    filtered = filter_records(all_records, protocol, source_ip, dest_ip)
    stats = compute_stats(filtered)
    stats["generated_count"] = generated_count

    return jsonify({
        "monitoring": monitoring_active,
        "records":    filtered,
        "stats":      stats,
    })


def generate_ai_data(num_packets=150):
    global generated_count
    count = len(generate_traffic_data(num_packets, output_file=DATA_FILE))
    generated_count += count
    return count


@app.route("/generate", methods=["POST"])
def generate_new_data():
    count = generate_ai_data(150)
    all_records = load_all_records()
    stats = compute_stats(all_records)
    return jsonify({"status": "generated", "count": count, "stats": stats})


if __name__ == "__main__":
    print("\n   Network Traffic Monitor is running!")
    print("  Open your browser and go to: http://127.0.0.1:5000\n")
    app.run(debug=True)
