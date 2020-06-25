import subprocess
import sys,os

def autossh():
    #Install packages
    print("[*] Installing Autossh Dependencies and Packages!")
    print("\n")
    subprocess.call("apt update", shell=True)
    subprocess.call("apt upgrade -y", shell=True)
    subprocess.call("apt install autossh python3-pip ssh -y", shell=True)
    subprocess.call("systemctl enable ssh", shell=True)
    subprocess.call("systemctl start ssh", shell=True)

    print("\n")
    #Checking for SSH keys and generating them if they do not exist
    print("[*] Checking for Existing SSH Keys...")
    if os.path.isfile('/root/.ssh/id_rsa'):
        print("[*] SSH Keys Already Exist. ")
    else:
        print("[*] Generating SSH Keys for root")
        subprocess.call("ssh-keygen", shell=True)
    print("\n")

    #Set up reverse SSH with autossh
    print("[*] Setting Up Connection Information")
    print("[!] Note: In order to copy the SSH key to the Public Server, the User on the Public Server Needs to Have Password Authentication Enabled Over SSH.")
    print("\n")
    server = input("Server IP or URL: ")
    rev_port = input("Select Port on Public Server for Port Forwarding to On-Site Machine: ")

    #ssh-copy-id
    print("[*] Copying SSH Key to Remote Machine")
    copy_id = "echo -n \"restrict,port-forwarding,permitopen=\\\"localhost:22\\\",permitlisten=\\\"" + rev_port + "\\\" \""
    copy_id += " | cat - /root/.ssh/id_rsa.pub | ssh root@" + server + " tee -a /home/autossh/.ssh/authorized_keys"
    subprocess.call(copy_id, shell=True)
    print("\n")

    #creating reverse SSH bash script
    print("[*] Creating Bash Script to Run on Boot")
    print("\n")
    if os.path.isfile('/root/reverse.sh'):
        print("[*] Bash Script Already Present")
    else:
        rev_ssh = '/usr/bin/autossh -f -N -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -R ' + rev_port + ':localhost:22 autossh@' + server
        f = open("/root/reverse.sh", "a")
        f.write("#!/bin/bash")
        f.write("\n\n")
        f.write(rev_ssh)
        f.close()
        subprocess.call("chmod +x /root/reverse.sh", shell=True)

    #Setting cronjob
    print("[*] Setting Connection to Launch on Boot Using Cron...")
    print("\n")
    #if os.path.isfile("/root/cronjob"):
    #    print("[*] Cronjob File Present")
    #    print("Check crontab -l To See If Script Set To Run On @reboot")
    #else:
    f2 = open("/root/cronjob", "a")
    f2.write("@reboot /bin/bash /root/reverse.sh\n\n")
    f2.close()
    subprocess.call("crontab /root/cronjob", shell=True)

    print("\n")
    print("\n")
    print("[*] Autossh Installation Complete")
    print("Please Reboot Machine to Check Connection Autolaunch on Boot")
