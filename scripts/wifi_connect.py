#script to automate wireless connections (both connecting and disconnecting) for remote wireless testing

import os
import subprocess
import argparse
import sys

INT = ""
ESSID = ""
USER = ""
PASS = ""
CONF = "/home/kali/wpa.conf"

def PrepInt():
    subprocess.call("ifmetric eth0 50", shell=True)
    subprocess.call("nmcli device set " + INT + " managed no", shell=True)

def DHCP():
    subprocess.call("sleep 5 && dhclient " + INT + " && ifmetric " + INT + " 500", shell=True)

def OPEN():
    PrepInt()
    subprocess.call("iwconfig " + INT + " essid " + ESSID, shell=True)
    DHCP()

def WEP():
    PrepInt()
    subprocess.call("iwconfig "+ INT + " essid " + ESSID + " key " + PASS + " enc on", shell=True)
    DHCP()

def WPA():
    PrepInt()
    subprocess.call("wpa_passphrase " + ESSID + " " + PASS + " > " + CONF, shell=True)
    subprocess.call("wpa_supplicant -B -i " + INT + " -c " + CONF, shell=True)
    DHCP()

def ENT():
    PrepInt()
    subprocess.call("echo 'network={\n scan_ssid=1\n eap=PEAP\n ssid=\" "+ ESSID + " \"\n key_mgmt=WPA-EAP\n identity=\"" + USER + "\"\n password=\"" + PASS + "\"\n phase1=\"peaplabel=0\"\n phase2=\"auth=MSCHAPV2\"\n}' > " + CONF, shell=True)
    subprocess.call("wpa_supplicant -B -i " + INT + " -c " + CONF, shell=True)
    DHCP()

def DisCon():
    subprocess.call("killall wpa_supplicant && iw dev " + INT + " disconnect && dhclient -r " + INT, shell=True)

if not os.geteuid() == 0:
    sys.exit("[!] Must Be Run As Root!")

parser = argparse.ArgumentParser(description="WiFi Connect/Disconnect Helper")

parser.add_argument('-i', '--interface', help='Specify Interface', type=str, required=True)
parser.add_argument('-s', '--ssid', help='Specify SSID', type=str)
parser.add_argument('-n', '--network', choices=['OPN', 'WEP', 'WPA', 'ENT'], help='Network type (open, WEP, WPA/WPA2, WPA-Enterprise)')
parser.add_argument('-k', '--key', help='WEP/WPA/WPA2/WPA-Enterprise Password', type=str)
parser.add_argument('-u', '--user', help='WPA-Enterprise username', type=str)

args = parser.parse_args()
INT = args.interface
ESSID = args.ssid
USER = args.user
PASS = args.key

if args.network == 'OPN':
    OPEN()
elif args.network == 'WEP':
    WEP()
elif args.network == 'WPA':
    WPA()
elif args.network == 'ENT':
    ENT()

