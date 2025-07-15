import os
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart #parsing, handling, generating emails
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
ALERT_RECIPIENT = os.getenv('ALERT_RECIPIENT')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
LOG_FILE = os.getenv('LOG_FILE', 'anomalies.log')

def send_anomaly_report():
    if not os.path.exists(LOG_FILE):
        num_anomalies = 0
    else:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            num_anomalies = sum(1 for _ in f)

    subject = f"Anomaly Report: {num_anomalies} anomalies detected"
    body = f"Hi,\n\nAttached is the anomalies.log file.\nNumber of anomalies found: {num_anomalies}\n\nRegards,\nYour IDS"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ALERT_RECIPIENT
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(LOG_FILE)}')
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, ALERT_RECIPIENT, msg.as_string())
        print(f"[+] Sent anomaly report with {num_anomalies} anomalies.")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

def schedule_email_reports():
    schedule.every(2).minutes.do(send_anomaly_report)
    print("Scheduler started. Will send anomaly report every 2 minutes.")
    while True:
        schedule.run_pending()
        time.sleep(1)
