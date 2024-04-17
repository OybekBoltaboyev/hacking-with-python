#!/usr/bin/env python

import optparse
import subprocess
import re
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interfece change its MAC address")
    parser.add_option("-m", "--new_mac", dest="new_mac", help="MAC address which will be changed to this ")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Aniq interfeys kiriting.")
    elif not options.new_mac:
        parser.error("[-] Aniq MAC manzil kiriting. ")
    return options

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    subprocess.call(["ifconfig"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
    mac_address_search_result=re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result.group(0):
        return mac_address_search_result.group(0)
    else:
        print("[-] Couldn't read MAC address.")
options= get_arguments()
current_mac=get_current_mac(options.interface)
print("Current MAC=" +str(current_mac))
change_mac(options.interface, options.new_mac)

current_mac=get_current_mac(options.interface)