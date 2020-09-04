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
        subprocess.call("apt update", shell=True)
        print("\n")
        #modifying SSH Connection Details
        print("[*] Modifying SSH Configuration To Allow for PasswordAuthentication")
        subprocess.call("""mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak &&
                cp configs/sshd_config /etc/ssh/sshd_config &&
                service ssh restart""", shell=True)
        #shutil.copyfile('configs/sshd_config', '/etc/ssh/sshd_config')
        #subprocess.call("cp configs/sshd_config /etc/ssh/sshd_config", shell=True)
        #subprocess.call("service ssh restart", shell=True)
        #Installing Webserver and Setting Up HTTPS
        print("\n")
        print("[*] Installing Apache and Certbot and Setting Up LetsEncrypt Certificates")
        print("\n")
        print("[*] Adding Apt Repositories")
        subprocess.call("add-apt-repository universe", shell=True)
        subprocess.call("add-apt-repository ppa:certbot/certbot", shell=True)
        subprocess.call("apt update", shell=True)
        subprocess.call("apt install apache2 software-properties-common certbot python3-certbot-apache -y", shell=True)
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
        subprocess.call("""rm /var/www/html/index.html &&
                cp scripts/index.html /var/www/html/index.html""", shell=True)
        #shutil.copyfile('scripts/index.html', '/var/www/html/index.html')
        print("\n")
        #Setting Root Password
        print("[*] Setting Up root Password")
        print("\n")
        subprocess.call("passwd", shell=True)
        #subprocess.call("mkdir /root/.ssh", shell=True)
        #subprocess.call("touch /root/.ssh/authorized_keys", shell=True)
        #subprocess.call("ssh-keygen", shell=True)
        
        #Setting up autossh user and SSH folder and authorized_keys file
        print("\n[*] Creating autossh user, SSH Directory")
        subprocess.call("""useradd autossh -m -s /usr/sbin/nologin &&
        usermod -p '*' autossh &&
        mkdir /home/autossh/.ssh &&
        touch /home/autossh/.ssh/authorized_keys &&
        chown -R autossh:autossh /home/autossh/.ssh &&
        chmod 600 /home/autossh/.ssh/authorized_keys""", shell=True)

        #restoring SSH configuration
        print("\n")
        print("[*] Restoring SSH Configuration")
        confirm = input("Run Setup Script for Onsite Device and Press ENTER When SSH Keys Have Been Uploaded to Public Server From Onsite Machine")
        subprocess.call("""mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak2 && 
                cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config &&
                service ssh restart""", shell=True)
        #shutil.copyfile("/etc/ssh/sshd_config.bak", "/etc/ssh/sshd_config")
        #subprocess.call("service ssh restart", shell=True)
        print("\n")
        print("[*] Complete!")
        print("\n")
