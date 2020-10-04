#!/usr/bin/env python3

import argparse,re,subprocess,uuid

def get_args():
    parser = argparse.ArgumentParser(description="Change MAC address of a particular interface")    
    parser.add_argument("interface",metavar="interface" ,help="set the interface")
    parser.add_argument("-s","--show",dest="show",action='store_true', help="show the MAC address and exit") 
    parser.add_argument("-m","--mac",dest="mac", metavar='', help="set the desired mac address in the form XX:XX:XX:XX:XX:XX")
    args = parser.parse_args()
    if(args.mac):
        if re.match("^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$", args.mac) is None:
            parser.error(f"{styles.FAIL_BOLD}[-] Invalid MAC Address, Please enter a desired mac address in the form XX:XX:XX:XX:XX:XX use --help for more info.{styles.DEF}") 
    return args

def get_mac():
    return (':'.join(re.findall('..', '%012x' % uuid.getnode()))) 

def change_mac(interface, mac):
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["sleep","0.25"])
    subprocess.call(["ifconfig",interface,"hw","ether",mac])
    subprocess.call(["sleep" ,"0.25"])
    subprocess.call(["ifconfig",interface,"up"])
    print(f"{styles.HEADER}[+] MAC address for {interface} has been changed to {get_mac()}{styles.DEF}")
    
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
    args = get_args()
    
    if(args.show):
        print("current MAC address: %s" % get_mac())
    elif(args.mac):
        change_mac(args.interface,args.mac)
  
if __name__ == '__main__':
    main()
    




