import csv
import time
from scapy.all import sniff, IP, TCP, UDP

# Network interface to capture from
INTERFACE = 'Wi-Fi' 

# CSV file to save training data
CSV_FILE = 'training_data.csv'

def extract_features(packet):
    if IP not in packet:
        return None
    ip_layer = packet[IP]
    proto = ip_layer.proto
    src_port = 0
    dst_port = 0
    if proto == 6 and TCP in packet:
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif proto == 17 and UDP in packet:
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport

    features = {
        'packet_length': len(packet),
        'src_port': src_port,
        'dst_port': dst_port,
        'protocol': proto,
        'timestamp': time.time()
    }
    return features

def write_header(csv_writer):
    csv_writer.writerow(['packet_length', 'src_port', 'dst_port', 'protocol', 'timestamp'])

def packet_handler(packet, csv_writer):
    features = extract_features(packet)
    if features:
        csv_writer.writerow([
            features['packet_length'],
            features['src_port'],
            features['dst_port'],
            features['protocol'],
            features['timestamp']
        ])
        print(f"Captured packet: {features}")

def main():
    with open(CSV_FILE, mode='w', newline='') as f:
        csv_writer = csv.writer(f)
        write_header(csv_writer)
        print(f"Starting packet capture on {INTERFACE}... Press Ctrl+C to stop and save.")
        sniff(iface=INTERFACE, prn=lambda pkt: packet_handler(pkt, csv_writer), store=False)

if __name__ == '__main__':
    main()
