# 🛡️ ShieldIQ - Intrusion Detection & Response System

ShieldIQ is an intelligent network security system that performs **real-time intrusion detection** using **Isolation Forest-based anomaly detection**, packet sniffing, and automated email alerts.

> Designed for proactive defense, anomaly logging, and rapid response in networked environments.

---

## 🚀 Features

- 📡 **Real-Time Packet Capture** using Scapy  
- 🧠 **Anomaly Detection** via trained Isolation Forest model  
- 📨 **Email Alerts** on suspected intrusions  
- 📊 **Anomaly Logs** with timestamped entries  
- 🌐 **Web Dashboard** (Flask) to monitor system status  

---

## 🛠️ Technologies Used

- **Python**
- **Scapy** – for low-level packet sniffing
- **Flask** – for the web interface
- **scikit-learn** – Isolation Forest anomaly detection
- **SMTP** – for sending email alerts
- **CSV Logs** – for tracking anomalies

---

## 📂 Project Structure

'''
pro/
├── app.py                      # Flask app for UI
├── capture.py                  # Packet capture & monitoring
├── train_model.py              # Train Isolation Forest model
├── isolation_forest_model.pkl  # Trained model file
├── feature_extraction.py       # Extracts features from packets
├── send_anomaly_report.py      # Email alert system
├── anomalies.log               # Stores logs of suspicious activity
├── templates/index.html        # Flask frontend
├── training_data.csv           # Training dataset
├── requirements.txt            # Python dependencies
└── .env                        # Contains SMTP and config credentials
'''

---

## ⚙️ Getting Started

### 1. Clone the repository

'''bash
git clone https://github.com/simran3475/YourRepoName.git
cd pro
'''

### 2. Set up environment variables

Create a '.env' file in the 'pro/' directory:

'''
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_email_password
RECEIVER_EMAIL=receiver@example.com
'''

### 3. Install dependencies

'''bash
pip install -r requirements.txt
'''

### 4. Train the model (if not already trained)

'''bash
python train_model.py
'''

### 5. Start packet capture and monitoring

'''bash
python capture.py
'''

### 6. Launch the Flask web interface

'''bash
python app.py
'''

---

## 📈 How It Works

1. **Capture:** Sniffs network packets using Scapy.
2. **Extract:** Converts packets into structured features.
3. **Detect:** Uses Isolation Forest to detect anomalies.
4. **Alert:** Sends real-time alerts and logs incidents.
5. **Visualize:** UI accessible at 'http://localhost:5000'.

---

## 🔍 Keywords

'Intrusion Detection', 'AI Security', 'Isolation Forest', 'Python Cybersecurity', 'Scapy Packet Sniffer',  
'Flask Dashboard', 'Network Monitoring', 'Email Alerts', 'Machine Learning Security'

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👩‍💻 Developed By

**Simran Sardana**  
B.Tech Computer Science | AI Security & Software Developer  
[GitHub](https://github.com/simran3475) · [LinkedIn](https://linkedin.com/in/simran-sardana)

