from scapy.all import sniff, IP, TCP, UDP

def extract_features(packet):
    if IP not in packet:
        return None
    proto = packet[IP].proto
    src_port = 0
    dst_port = 0
    if proto == 6 and TCP in packet:
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif proto == 17 and UDP in packet:
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
    return {
        'packet_length': len(packet),
        'src_port': src_port,
        'dst_port': dst_port,
        'protocol': proto
    }

def packet_callback(packet):
    features = extract_features(packet)
    if features:
        print(f"Captured packet features: {features}")

if __name__ == "__main__":
    INTERFACE = "Wi-Fi" 
    print(f"Sniffing on interface: {INTERFACE}")
    sniff(iface=INTERFACE, prn=packet_callback, store=0)
