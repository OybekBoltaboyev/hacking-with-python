import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=sniffer_packet)

def sniffer_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print(str(url))
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)

sniff("eth0")