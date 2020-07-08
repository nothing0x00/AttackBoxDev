import subprocess
import os
import argparse
import sys

if not os.geteuid() == 0:
    sys.exit("[!] Must Be Run As Root!")

parser = argparse.ArgumentParser(description="Network Interface Monitor Mode Setup")
subs = parser.add_subparsers()
subs.required = True
subs.dest = "monitor or managed"

monitor_parser = subs.add_parser("monitor", help="Set An Interface Into Monitor Mode Safely")
monitor_parser.add_argument('-i', '--interface', help='Specify Interface to Set Into Monitor Mode')
monitor_parser.set_defaults(mode="monitor")

managed_parser = subs.add_parser("managed", help="Set an Interface Into Managed Mode")
managedgroup = managed_parser.add_mutually_exclusive_group()
managedgroup.add_argument('-i', '--interface', help='Specify Interface to Set Into Monitor Mode')
managed_parser.set_defaults(mode="managed")

args = parser.parse_args()

def monitor():
    interface = args.interface
    if str(interface) == "None":
        print("[!] Specify an Interface in the -i Option")
        sys.exit()
    else:
        print("[*] Shutting down " + str(interface))
        nmcli = "nmcli device set %s managed no" % interface
        subprocess.call(nmcli, shell=True)
        print("\n")
        print("[*] Putting %s Into Monitor Mode" % str(interface))
        airmon = "airmon-ng start " + interface
        subprocess.call(airmon, shell=True)

def managed():
    interface = args.interface
    if str(interface) == "None":
        print("[!] Specify an Interface in the -i Option")
        sys.exit()
    else:
        print("[*] Taking %s Out of Monitor Mode " % str(interface))
        airmon = "airmon-ng stop " + interface
        subprocess.call(airmon, shell=True)
        print("\n")
        print("[*] Restarting Interface")
        interface_new = str(interface)
        managed = interface_new.replace('mon', '')
        nmcli = "nmcli device set %s managed yes" % managed
        subprocess.call(nmcli, shell=True)

if args.mode == "monitor":
    monitor()

if args.mode == "managed":
    managed()
