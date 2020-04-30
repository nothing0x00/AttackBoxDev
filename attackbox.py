import subprocess
import sys,os
import modules.internal_pentest as internal
import modules.wireless as wireless
import modules.autossh as autossh
import modules.vnc as vnc
import argparse


print('''

   ___         ________                 ____                 _ __
  / _ \___ ___/ /_  __/__ ___ ___ _    / __/__ ______ ______(_) /___ __
 / , _/ -_) _  / / / / -_) _ `/  ' \  _\ \/ -_) __/ // / __/ / __/ // /
/_/|_|\__/\_,_/ /_/  \__/\_,_/_/_/_/ /___/\__/\__/\_,_/_/ /_/\__/\_, /
                                                                /___/

Internal Pentest and Remote Wireless Testing Dropbox Installation Script
''')

if not os.geteuid() == 0:
    sys.exit("[!] Must Be Run As Root!")

print("Before Continuing Make Sure That DNS is Set for Remote Server and SSH Access Has Been Established (Needed for Transferring SSH Keys)")
input("Press ENTER to Continue")
print("\n")

#argument structure

parser = argparse.ArgumentParser(description='Attackbox setup')

parser.add_argument('-a', '--autossh', action='store_true', help='Installs and configures autossh')
parser.add_argument('-i', '--internal', action='store_true', help='Installs tools for a internal pen test')
parser.add_argument('-w', '--wireless', action='store_true', help='Installs tools for a wireless pen test')
parser.add_argument('-v', '--vnc', action='store_true', help='Installs and configures VNC')

args=parser.parse_args()

if args.internal:
    internal.internal()
if args.wireless:
    wireless.wireless()
if args.autossh:
    autossh.autossh()
if args.vnc:
    vnc.vnc()


## TODO:
# Install additional requested software
# Polling webserver Functionality
# automate SSH configuration
# RPi module
