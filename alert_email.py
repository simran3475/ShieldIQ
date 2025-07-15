import smtplib
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD, ALERT_RECIPIENT
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
ALERT_RECIPIENT = os.getenv('ALERT_RECIPIENT')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
LOG_FILE = os.getenv('LOG_FILE', 'anomalies.log')


def send_email_alert(anomaly_info):
    subject = f"Network Anomaly Detected: {anomaly_info['src_ip']}"
    body = f"""
Anomaly Detected on Network:

Source IP: {anomaly_info['src_ip']}
Destination IP: {anomaly_info['dst_ip']}
Packet Length: {anomaly_info['packet_length']}
Protocol: {anomaly_info['protocol']}
Anomaly Score: {anomaly_info['anomaly_score']}

Please investigate immediately.
"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ALERT_RECIPIENT

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"[+] Email alert sent for {anomaly_info['src_ip']}")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")
