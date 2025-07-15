from scapy.all import IP, TCP, UDP, sniff

def extract_features(packet):
    if IP not in packet:
        return None

    ip_layer = packet[IP]
    proto = ip_layer.proto
    src_port = 0
    dst_port = 0

    # Extract ports if TCP or UDP
    if proto == 6 and TCP in packet:  # TCP
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif proto == 17 and UDP in packet:  # UDP
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport

    features = {
        'packet_length': len(packet),
        'src_port': src_port,
        'dst_port': dst_port,
        'protocol': proto
    }
    return features
