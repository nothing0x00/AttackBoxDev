#script to automate wireless connections (both connecting and disconnecting) for remote wireless testing

import os
import subprocess
import argparse
import sys

INT = ""
SSID = ""
USER = ""
PASS = ""
CONF = "/home/kali/wpa.conf"

#def ENT():
#    PrepInt()
#    subprocess.call("echo 'network={\n scan_ssid=1\n eap=PEAP\n ssid=\" "+ SSID + " \"\n key_mgmt=WPA-EAP\n identity=\"" + USER + "\"\n password=\"" + PASS + "\"\n phase1=\"peaplabel=0\"\n phase2=\"auth=MSCHAPV2\"\n}' > " + CONF, shell=True)
#    subprocess.call("wpa_supplicant -B -i " + INT + " -c " + CONF, shell=True)

if not os.geteuid() == 0:
    sys.exit("[!] Must Be Run As Root!")

parser = argparse.ArgumentParser(description="WiFi Connect/Disconnect Helper")

parser.add_argument('-i', '--interface', help='Specify Interface', type=str, required=True)
parser.add_argument('-s', '--ssid', help='Specify SSID', type=str)
parser.add_argument('-e', '--enterprise', help='Network type WPA-Enterprise', action='store_true')
parser.add_argument('-t', '--weptype', choices=['key','phrase'], help='If WEP encryption, specify HEX key or passphrase.')
parser.add_argument('-p', '--password', help='WEP/WPA/WPA2/WPA-Enterprise Passphrase or Key', type=str)
parser.add_argument('-u', '--user', help='WPA-Enterprise username', type=str)
parser.add_argument('-H', '--hidden', help='SSID hidden', action='store_true')

parser.add_argument('-X', '--kill', help='Kill WiFi Connection', action='store_true')

args = parser.parse_args()
INT = args.interface
SSID = args.ssid
USER = args.user
PASS = args.password
cmd = ''

#set metric of eth0 to low value to establish higher precedence for routing
subprocess.call('nmcli con mod uuid $(nmcli -f UUID,DEVICE -p c | grep eth0 | cut -d " " -f 1) ipv4.route-metric 50', shell=True)

if args.kill:
    cmd = 'nmcli con delete id WiFi-' + INT
elif args.enterprise and args.interface and args.ssid and args.user and args.password:
    subprocess.call('nmcli con delete id WiFi-' + INT, shell=True)
    cmd = 'nmcli con add type wifi ifname wlan1 con-name WiFi-' + INT + ' ssid ' + SSID
    cmd = cmd + ' && nmcli con mod WiFi-' + INT 
    cmd = cmd + ' ipv4.method auto 802-1x.eap peap 802-1x.phase2-auth mschapv2 802-1x.identity ' + USER 
    cmd = cmd + ' 802-1x.password ' + PASS + ' wifi-sec.key-mgmt wpa-eap connection.autoconnect no'
    cmd = cmd + ' && nmcli con up WiFi-' + INT
else:
    if args.interface and args.ssid:
        #delete existing connection if one already exists
        subprocess.call('nmcli con delete id WiFi-' + INT, shell=True)

        #build connection command
        cmd = 'nmcli d wifi connect ' + SSID + ' ifname ' + INT + ' name WiFi-' + INT
        if args.password:
            cmd = cmd + ' password ' + PASS
            if args.weptype == 'key':
                cmd = cmd + ' wep-key-type key'
            elif args.weptype == 'phrase':
                cmd = cmd + ' wep-key-type phrase'
        if args.hidden:
            cmd = cmd + ' hidden yes'
        
        #make sure the new connection does not autoconnect on reboot
        cmd = cmd + ' && nmcli con mod WiFi-' + INT + ' connection.autoconnect no'

print(cmd)
subprocess.call(cmd, shell=True)
