import scapy.all as scapy
import argparse
from mac_vendor_lookup import MacLookup, VendorNotFoundError
# mac=MacLookup()
# mac.update_vendors() # run it if connection is good
def scan(ip):
    arp_request=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast=broadcast/arp_request
    answered_list=scapy.srp(arp_request_broadcast, timeout=1,verbose=False)[0]

    clients_list=[]
    for element in answered_list:
        mac_address=element[1].hwsrc
        try:
            vendor=MacLookup().lookup(mac_address)
        except VendorNotFoundError:
            vendor="Unknown"

    clients_dict={
        "IP":element[1].psrc,
        "MAC":mac_address,
        "Vendor":vendor
    }
    clients_list.append(clients_dict)
    return clients_list

def print_result(result_list):
    print("IP\t\tMAC\t\tVendor")
    for client in result_list:
        print(client["IP"]+"\t\t"+client["MAC"]+"\t\t"+client["Vendor"])

def target_ip():
    parser=argparse.ArgumentParser()
    parser.add_argument('-t','--target',dest='target',help="Target IP/IP range.")
    options=parser.parse_args()
    return options

options=target_ip()
scan_result=scan(options.target)
print_result(scan_result)
