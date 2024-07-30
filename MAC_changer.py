import subprocess
import argparse
import re
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="MAC manzilini o'zgartirish uchun interfeys")
    parser.add_argument("-n", "--new_mac", dest="new_mac", help="Yangi MAC manzil")
    options=parser.parse_args()
    if not options.new_mac:
        parser.error("Iltimos yangi MAC manzilni to'g'ri kiriting.")
    elif not options.interface:
        parser.error("Iltimos interfeysni to'g'ri kiriting.")
    return options
def change_mac(interface,new_mac):
    print("MAC manzil yangisiga o'zgaryapti! ")
    subprocess.call("ifconfig " + interface +" down", shell=True)
    subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
    subprocess.call("ifconfig " +interface+ " up", shell=True)
def get_current_mac(interface):
    ifconfig_result=subprocess.check_output(["ifconfig",interface])
    mac_changer_result=re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig_result))
    if mac_changer_result:
        return (mac_changer_result.group())
    else:
        print("[+] MAC manzilni o'qib bo'lmadi")
def reset_mac(interface):
    print(f"{interface} interfeysi uchun MAC amnzil dastlabki holatga qaytarilyapti!")
    subprocess.call(f"ifconfig {interface} down", shell=True)
options=get_arguments()

current_mac=get_current_mac(options.interface)
print("joriy MAC = " +str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
answer=input("Tekshirasizmi? (h/y)\n--> ")
if not answer=='y':
    subprocess.call("ifconfig " + options.interface, shell=True)
else:
    print("e'tiboringiz uchun rahmat")
