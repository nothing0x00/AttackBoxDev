import subprocess
import sys,os

def vnc():
    #Install packages
    print("[*] Installing VNC Dependencies and Packages!")
    print("\n")
    subprocess.call("apt update", shell=True)
    #subprocess.call("apt upgrade -y", shell=True)
    subprocess.call("apt install xfce4 xfce4-goodies xorg dbus-x11 x11-xserver-utils tigervnc-standalone-server tigervnc-common -y", shell=True)
    print("\n")
    print("\n")
    user = input("Username to run VNC as: ")
    #Checking for SSH keys and generating them if they do not exist
    print("[*] Checking for existing xstartup configuration...")
    if user == 'root':
        userpath = '/root/.vnc/'
    else:
        userpath = '/home/'+user+'/.vnc/'
    if os.path.isfile(userpath+'xstartup'):
        print("[*] Xstartup Already Exists. ")
    else:
        print("[*] Create Xstartup settings for user: " + user)
        if os.path.exists(userpath):
            subprocess.call("cp configs/xstartup " + userpath, shell=True)
        else:
            subprocess.call("mkdir " + userpath, shell=True)
            subprocess.call("cp configs/xstartup " + userpath, shell=True)
        subprocess.call("chmod u+x " + userpath + "xstartup", shell=True)
    #set default vnc password to kali
    if os.path.isfile(userpath+'passwd'):
        print("[*] VNC passwd already exists.")
    else:
        subprocess.call("echo 'kali' | vncpasswd -f > " + userpath + "passwd", shell=True)
        subprocess.call("chmod 600 " + userpath + "passwd", shell=True)
        subprocess.call("chown -R " + user + ":" + user + " " + userpath, shell=True)
    print("\n")

    print("[*] Checking for existing vncserver service...")
    print("\n")

    if os.path.isfile('/etc/systemd/system/vncserver@.service'):
        print("[*] VNC service already exists")
    else:
        print("[*] Create, enable, launch VNC service for user: " + user)
        subprocess.call("cp configs/vncserver@.service /etc/systemd/system/vncserver@.service", shell=True)
        subprocess.call("sed -i 's/kali/" + user + "/g' /etc/systemd/system/vncserver@.service", shell=True)
        subprocess.call("systemctl daemon-reload", shell=True)
        subprocess.call("systemctl enable vncserver@1.service", shell=True)
        subprocess.call("systemctl start vncserver@1.service", shell=True)
    print("\n\n[*] To connect via VNC run the following from your client:")
    print("ssh -N -L 5900:localhost:5901 -o ProxyCommand=""ssh -W %h:%p username@public.jump.server"" kali@localhost -p 10999")
    print("vncviewer localhost\n\n")
