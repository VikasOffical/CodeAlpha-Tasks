from scapy.all import sniff

def process_packet(pkt):
    print(f"\n[+] Captured Packet: {pkt.summary()}")

    if pkt.haslayer('IP'):
        src_ip = pkt['IP'].src
        dst_ip = pkt['IP'].dst
        print(f"    - IP Source: {src_ip}, IP Destination: {dst_ip}")

    if pkt.haslayer('TCP'):
        src_port = pkt['TCP'].sport
        dst_port = pkt['TCP'].dport
        print(f"    - TCP Source Port: {src_port}, TCP Destination Port: {dst_port}")

    if pkt.haslayer('UDP'):
        src_port = pkt['UDP'].sport
        dst_port = pkt['UDP'].dport
        print(f"    - UDP Source Port: {src_port}, UDP Destination Port: {dst_port}")


print("=== Packet Sniffing Started ===")

sniff(prn=process_packet, store=False, count=10)  
