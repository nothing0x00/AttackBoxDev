import subprocess
import sys,os
import modules.public as public
import modules.internal_pentest as internal
import modules.wireless as wireless
import modules.autossh as autossh
import modules.vnc as vnc
import modules.httpc2_setup as httpc2_setup
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

parser.add_argument('-p', '--public', action='store_true', help='Installs and Configures Public C2 Server')
parser.add_argument('-a', '--autossh', action='store_true', help='Installs and configures autossh')
parser.add_argument('-i', '--internal', action='store_true', help='Installs tools for a internal pen test')
parser.add_argument('-w', '--wireless', action='store_true', help='Installs tools for a wireless pen test')
parser.add_argument('-v', '--vnc', action='store_true', help='Installs and configures VNC')
parser.add_argument('-c', '--c2', action='store_true', help="Installs and Configures HTTP Command Polling")
parser.add_argument('-r', '--rpi', action='store_true', help="Installs and Configures Raspberry Pi Physical Pentest Dropbox")

args=parser.parse_args()

if args.public:
    public.server()
if args.internal:
    internal.internal()
if args.wireless:
    wireless.wireless()
if args.autossh:
    autossh.autossh()
if args.vnc:
    vnc.vnc()
if args.c2:
    httpc2_setup.httpc2()
if args.rpi:
    internal.internal()
    autossh.autossh()
    httpc2_setup.httpc2()
