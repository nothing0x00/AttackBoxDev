import subprocess
import sys,os

print('''

   ___         ________                 ____                 _ __
  / _ \___ ___/ /_  __/__ ___ ___ _    / __/__ ______ ______(_) /___ __
 / , _/ -_) _  / / / / -_) _ `/  ' \  _\ \/ -_) __/ // / __/ / __/ // /
/_/|_|\__/\_,_/ /_/  \__/\_,_/_/_/_/ /___/\__/\__/\_,_/_/ /_/\__/\_, /
                                                                /___/

Internal Pentest and Remote Wireless Testing Dropbox Installation Script
''')

print("[*] Internal Penetration Test VM Configuration Script")
print("[*] Before Continuing Generate SSH Keys and Transfer Public Key to Public Server")
keys = input("Press ENTER when SSH Keys Have Been Transfered to Public Server")
print("\n")
print("[*] Installing and Configuring System")
print("\n")
print("[*] Installing Dependencies and Packages!")
print("\n")
subprocess.call("apt update", shell=True)
subprocess.call("apt upgrade -y", shell=True)
subprocess.call("apt install kali-tools-database kali-tools-headless kali-tools-information-gathering kali-tools-passwords kali-tools-post-exploitation -y", shell=True)
print("[*] Installing Source Files for CrackMapExec, Responder, MITM6 and Impacket and Installing Dependencies")
subprocess.call("git clone https://github.com/SecureAuthCorp/impacket.git", shell=True)
subprocess.call("git clone https://github.com/fox-it/mitm6.git", shell=True)
subprocess.call("pip3 install -r mitm6/requirements.txt", shell=True)
subprocess.call("git clone https://github.com/lgandx/Responder.git", shell=True)
subprocess.call("apt install libssl-dev libffi-dev python-dev build-essential -y", shell=True)
subprocess.call("git clone --recursive https://github.com/byt3bl33d3r/CrackMapExec", shell=True)
subprocess.call("apt remove crackmapexec", shell=True)
subprocess.call("python3 CrackMapExec/setup.py install", shell=True)
print("\n")

print("[*] Installing Autossh Dependencies and Packages!")
print("\n")
subprocess.call("apt update", shell=True)
subprocess.call("apt upgrade -y", shell=True)
subprocess.call("apt install autossh python3-pip ssh -y", shell=True)
subprocess.call("systemctl enable ssh", shell=True)
subprocess.call("systemctl start ssh", shell=True)

print("\n")

#Set up reverse SSH with autossh
print("[*] Setting Up Connection Information")
print("\n")
server = input("Server IP or URL: ")
rev_port = input("Select Port on Public Server for Port Forwarding to On-Site Machine: ")

#creating reverse SSH bash script
print("[*] Creating Bash Script to Run on Boot")
print("\n")
if os.path.isfile('/root/reverse.sh'):
    print("[*] Bash Script Already Present")
else:
    rev_ssh = '/usr/bin/autossh -f -N -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -R ' + rev_port + ':localhost:22 root@' + server
    f = open("/root/reverse.sh", "a")
    f.write("#!/bin/bash")
    f.write("\n\n")
    f.write(rev_ssh)
    f.close()
    subprocess.call("chmod +x /root/reverse.sh", shell=True)

#Setting cronjob
print("[*] Setting Connection to Launch on Boot Using Cron...")
print("\n")
if os.path.isfile("/root/cronjob"):
    print("[*] Cronjob File Present")
    print("Check crontab -l To See If Script Set To Run On @reboot")
else:
    f2 = open("/root/cronjob", "w")
    f2.write("@reboot /bin/bash /root/reverse.sh\n\n")
    f2.close()
    subprocess.call("crontab /root/cronjob", shell=True)

print("\n")
print("[*] Autossh Installation Complete")
print("Please Reboot Machine to Check Connection Autolaunch on Boot")
