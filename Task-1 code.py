from scapy.all import sniff 
def packet_callback(packet):
    print(f"Packet: {packet.summary()}")
    if packet.haslayer('IP'):
        ip_src = packet['IP'].src
        ip_dst = packet['IP'].dst
        print(f"Source IP: {ip_src}, Destination IP: {ip_dst}")
        
    if packet.haslayer('TCP'):
        tcp_src_port = packet['TCP'].sport
        tcp_dst_port = packet['TCP'].dport
        print(f"Source Port: {tcp_src_port}, Destination Port: {tcp_dst_port}")
        
    if packet.haslayer('UDP'):
        udp_src_port = packet['UDP'].sport
        udp_dst_port = packet['UDP'].dport
        print(f"Source Port: {udp_src_port}, Destination Port: {udp_dst_port}")
# Start sniffing packets
print("Starting packet capture...")

sniff(prn=packet_callback, store=0, count=10)  # Capture 10 packets