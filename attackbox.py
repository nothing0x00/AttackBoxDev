import subprocess
import sys,os
import modules.publicserver as public
import modules.internal_pentest as internal
import modules.wireless as wireless
import modules.autossh as autossh
import modules.vnc as vnc
import modules.httpc2_setup as httpc2_setup
import modules.clientconfig as client
import argparse


def clientcron():
    print("\n[*]Installing cronjobs\n")
    subprocess.call("crontab /root/cronjob", shell=True)

def update():
    print("Updating packages\n")
    subprocess.call("apt upgrade -y", shell=True)

print('''


   _____   __    __                 __   __________              
  /  _  \_/  |__/  |______    ____ |  | _\______   \ _______  ___
 /  /_\  \   __\   __\__  \ _/ ___\|  |/ /|    |  _//  _ \  \/  /
/    |    \  |  |  |  / __ \\  \___|    < |    |   (  <_> >    < 
\____|__  /__|  |__| (____  /\___  >__|_ \|______  /\____/__/\_ \
        \/                \/     \/     \/       \/            \/

Internal Pentest and Remote Wireless Testing Dropbox Installation Script
''')

if not os.geteuid() == 0:
    sys.exit("[!] Must Be Run As Root!")

#argument structure

parser = argparse.ArgumentParser(description='AttackBox setup')

subs = parser.add_subparsers()
subs.required = True
subs.dest = 'public or client or custom'


public_parser = subs.add_parser('public', help='Installs and Configures Public C2 Server')
public_parser.set_defaults(mode='public')

client_parser = subs.add_parser('client', help='Installs and Configures Specific Client System')
buildgroup = client_parser.add_mutually_exclusive_group()
buildgroup.add_argument('--all', action='store_true', help="Install and configure all client modules")
buildgroup.add_argument('--rpi', action='store_true', help="Installs and configures Raspberry Pi Physical Pentest Dropbox")
buildgroup.add_argument('--vm', action='store_true', help="Installs and configures Pentest Virtual Machine")
buildgroup.add_argument('--nuc', action='store_true', help="Installs and confgures Intel NUC Physical Pentest Dropbox")
client_parser.set_defaults(mode='client')

custom_parser = subs.add_parser('custom', help='Installs and configures selected modules')
custom_parser.add_argument('-a', '--autossh', action='store_true', help='Installs and configures autossh')
custom_parser.add_argument('-i', '--internal', action='store_true', help='Installs tools for a internal pen test')
custom_parser.add_argument('-w', '--wireless', action='store_true', help='Installs tools for a wireless pen test')
custom_parser.add_argument('-v', '--vnc', action='store_true', help='Installs and configures VNC')
custom_parser.add_argument('-c', '--c2', action='store_true', help="Installs and configures HTTP Command Polling")
custom_parser.add_argument('-l', '--client', action='store_true', help="Installs client-side post-deployment configuration script")
custom_parser.add_argument('-u', '--update', action='store_true', help="Installs updates")
custom_parser.set_defaults(mode='custom')
args=parser.parse_args()

print("Before Continuing Make Sure That DNS is Set for Remote Server and SSH Access Has Been Established (Needed for Transferring SSH Keys)")
input("Press ENTER to Continue")
print("\n")

if args.mode == 'public':
    public.server()
elif args.mode == 'client':
    if args.all:
        update()
        internal.internal()
        wireless.wireless()
        autossh.autossh()
        vnc.vnc()
        httpc2_setup.httpc2()
        client.clientconfig()
        clientcron()
    elif args.vm:
        internal.internal()
        print("\n\n[*] If this VM will be distributed to multiple clients, use a 'test' public server value during autossh setup.")
        input("Press ENTER to Continue")
        autossh.autossh()
        vnc.vnc()
        client.clientconfig()
        clientcron()
        print("\n\n[*] If this VM will be distributed to multiple clients, backup the root users public SSH key and manually install on the appropriate public server.")
        print("[*] Additionally, the client must run 'Callback Server Configuration' from the applications menu to provide the appropriate remote public server and port information.\n\n")
    elif args.nuc:
        internal.internal()
        wireless.wireless()
        autossh.autossh()
        clientcron()
    elif args.rpi:
        internal.internal()
        autossh.autossh()
        httpc2_setup.httpc2()
        clientcron()
elif args.mode == 'custom':
    if args.internal:
        internal.internal()
    if args.wireless:
        wireless.wireless()
    if args.autossh:
        autossh.autossh()
        clientcron()
    if args.vnc:
        vnc.vnc()
    if args.c2:
        httpc2_setup.httpc2()
    if args.client:
        client.clientconfig()
    if args.update:
        update()

print("\n")
print("[*] Installation Complete!")
print("\n")
