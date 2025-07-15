import logging

LOG_FILE = 'anomalies.log'

# Set up logging to both file and terminal
logger = logging.getLogger('NetworkIDS')
logger.setLevel(logging.INFO)

# File handler
fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

def log_anomaly(anomaly_info):
    msg = (f"Anomaly detected - SrcIP: {anomaly_info['src_ip']}, "
           f"DstIP: {anomaly_info['dst_ip']}, "
           f"Packet Length: {anomaly_info['packet_length']}, "
           f"Protocol: {anomaly_info['protocol']}, "
           f"Anomaly Score: {anomaly_info['anomaly_score']:.4f}")
    logger.warning(msg)
