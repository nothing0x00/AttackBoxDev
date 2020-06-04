import subprocess
import os,sys
import shutil

def server():
    print("\n")
    print("[*] Checking if User is Root or Sudo")
    print("\n")
    if not os.geteuid() == 0:
        sys.exit("[!] Must Be Run As Root!")
    else:
        pwd = str(subprocess.call("pwd", shell=True))
        #Updating Repositories and Upgrading System
        print("[*] Updating Apt Repositories and Upgrading Packages")
        subprocess.call("apt update && apt upgrade -y", shell=True)
        print("\n")
        #modifying SSH Connection Details
        print("[*] Modifying SSH Configuration To Allow for PasswordAuthentication")
        subprocess.call("mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak", shell=True)
        #error here, file not moved properly
        #ssh_config = pwd + "/configs/sshd_config"
        #ssh_config_cp = "cp " + pwd + " /etc/ssh/"
        #subprocess.call(ssh_config_cp, shell=True)
        #subprocess.call("service ssh restart", shell=True)
        shutil.copyfile('configs/sshd_config', '/etc/ssh/sshd_config')
        #Installing Webserver and Setting Up HTTPS
        print("\n")
        print("[*] Installing Apache and Certbot and Setting Up LetsEncrypt Certificates")
        print("\n")
        print("[*] Adding Apt Repositories")
        subprocess.call("add-apt-repository universe", shell=True)
        subprocess.call("add-apt-repository ppa:certbot/certbot", shell=True)
        subprocess.call("apt update", shell=True)
        subprocess.call("apt install apache2 software-properties-common certbot python-certbot-apache -y", shell=True)
        print("\n")
        dns = input("Is DNS Set Up For This IP (Y or N)?: ")
        if dns == "y" or "Y":
            subprocess.call("certbot --apache", shell=True)
        else:
            print("[!] Please Set DNS and Then Run certbot --apache to Generate Certificate")
        print("\n")
        print("[*] Setting Up Webpage for Command Transmission")
        print("\n")
        subprocess.call("touch /var/www/html/commands.txt", shell=True)
        print("Edit /var/www/html/commands.txt To Send Commands to the Onsite Device")
        print("\n")
        print("Setting Dummy Homepage for Webserver")
        subprocess.call("rm /var/www/html/index.html", shell=True)
        #index_location = pwd + "/scripts/index.html"
        #index_location_cmd = "cp " + index_location + " /var/www/html"
        #subprocess.call(index_location_cmd, shell=True)
        shutil.copyfile('scripts/index.html', '/var/www/html/index.html')
        print("\n")
        #Setting Root Password and SSH keys
        print("[*] Setting Up root Password, SSH Directory and SSH Keys")
        print("\n")
        subprocess.call("passwd", shell=True)
        subprocess.call("mkdir /root/.ssh", shell=True)
        subprocess.call("touch /root/.ssh/authorized_keys", shell=True)
        subprocess.call("ssh-keygen", shell=True)
        #restoring SSH configuration
        print("\n")
        print("[*] Restoring SSH Configuration")
        confirm = input("Run Setup Script for Onsite Device and Press ENTER When SSH Keys Have Been Uploaded to Public Server From Onsite Machine")
        subprocess.call("mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak2", shell=True)
        shutil.copyfile("/etc/ssh/sshd_config.bak", "/etc/ssh/sshd_config")
        subprocess.call("service ssh restart", shell=True)
        print("\n")
        print("[*] Complete!")
        print("\n")
