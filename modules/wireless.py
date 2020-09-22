import subprocess
import os,sys

def wireless():
    #Install packages
    print("[*] Installing Dependencies and Packages!")
    print("\n")
    subprocess.call("apt update", shell=True)
    subprocess.call("apt install kali-tools-802-11 kali-tools-headless kali-tools-passwords kali-tools-wireless hcxdumptool hcxtools hostapd libssl-dev libffi-dev build-essential python3-pyqt5 ifmetric -y", shell=True)
    subprocess.call("git clone https://github.com/P0cL4bs/wifipumpkin3.git", shell=True)
    subprocess.call("git clone https://github.com/derv82/wifite2.git", shell=True)
    subprocess.call("git clone https://github.com/s0lst1c3/eaphammer.git", shell=True)
    subprocess.call("./eaphammer/kali-setup", shell=True)

    print("\n")


    print("[*] Installation Complete")
