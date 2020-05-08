import subprocess
import os,sys

def wireless():
    #Install packages
    print("[*] Installing Dependencies and Packages!")
    print("\n")
    subprocess.call("apt update", shell=True)
    subprocess.call("apt upgrade -y", shell=True)
    subprocess.call("apt install kali-tools-802-11 kali-tools-headless kali-tools-passwords kali-tools-wireless hcxdumptool hcxtools -y", shell=True)        
    subprocess.call("git clone https://github.com/v1s1t0r1sh3r3/airgeddon.git", shell=True)
    subprocess.call("chmod +x airgeddon/airgeddon.sh", shell=True)
    subprocess.call("git clone https://github.com/derv82/wifite2.git", shell=True)
    subprocess.call("git clone https://github.com/s0lst1c3/eaphammer.git", shell=True)
    subprocess.call("./eaphammer/kali-setup", shell=True)

    print("\n")


    print("[*] Installation Complete")
