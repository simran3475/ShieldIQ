import time
import pandas as pd
import joblib #parallel computing
from scapy.all import sniff, IP
from feature_extraction import extract_features
from alert_email import send_email_alert
from config import MODEL_FILE, ANOMALY_SCORE_THRESHOLD, LOG_FILE, NETWORK_INTERFACE
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import logging
from loggingt import log_anomaly
from flask_cors import CORS #cross origin resource sharing
import threading
import schedule
import time
from send_anomaly_report import send_anomaly_report


# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(message)s')

# Load trained model
model = joblib.load(MODEL_FILE)

# Flask app and SocketIO for real-time graph
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
# Store anomalies for visualization
anomaly_data = []

def log_and_emit_anomaly(info):
    log_msg = f"Anomaly: SrcIP={info['src_ip']} DstIP={info['dst_ip']} Length={info['packet_length']} Score={info['anomaly_score']:.4f}"
    log_anomaly(info)
    print(log_msg)
    logging.info(log_msg)
    anomaly_data.append(info)
    # Emit to frontend
    print(f"Emitting anomaly to frontend: {info}")
    socketio.emit('new_anomaly', info)

def packet_callback(packet):
    features = extract_features(packet)
    if features is None:
        print("Packet skipped: no IP layer")
        return

    print(f"Packet captured: {features}")  # Debug print

    df = pd.DataFrame([features])
    score = model.decision_function(df)[0]
    print(f"Anomaly score: {score}")

    if score < ANOMALY_SCORE_THRESHOLD:
        # Extract IP info
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        anomaly_info = {
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'packet_length': features['packet_length'],
            'protocol': features['protocol'],
            'anomaly_score': score
        }
        log_and_emit_anomaly(anomaly_info)
        send_email_alert(anomaly_info)

@app.route('/')
def index():
    return render_template('index.html')

def start_sniffing():
    sniff(iface=NETWORK_INTERFACE, prn=packet_callback, store=0)
@app.route('/test_emit')
def test_emit():
    socketio.emit('new_anomaly', {'anomaly_score': -0.5})
    return "Emitted test anomaly."


def schedule_email_reports():
    schedule.every(2).minutes.do(send_anomaly_report)
    print("Scheduler started. Will send anomaly report every 2 minutes.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':

    scheduler_thread = threading.Thread(target=schedule_email_reports, daemon=True)
    scheduler_thread.start()
    # Run sniffing in background thread
    import eventlet
    eventlet.monkey_patch()
    sniff_thread = threading.Thread(target=start_sniffing, daemon=True)
    sniff_thread.start()

    # Run Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000)
