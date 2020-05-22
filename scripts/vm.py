#Standalone script to install and configure virtual machine images to connect to reverse ssh

pre-generate the keys and pre-transfer them to the public Server
add code to install tooling from internal_pentest
import subprocess
import sys,os


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
