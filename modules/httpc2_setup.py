import os
import subprocess

#set httpc2.py to run on boot
def httpc2():
    print("\n")
    print("[*] Setting up HTTP Command Polling")
    print("\n")
    print("[*] Installing Dependencies")
    subprocess.call("sudo pip3 install requests schedule")
    print("\n")
    print("[*] Setting up HTTP command polling to run on boot")
    print("Make sure to edit the /bin/httpc2/httpc2.py to insert the proper URL into the r parameter")
    cntnue = input("Press ENTER once URL has been modified in httpc2.py")
    print("\n")
    subprocess.call("mkdir /bin/httpc2", shell=True)
    subprocess.call("mv scripts/httpc2.py /bin/httpc2/", shell=True)
    print("\n")
    if os.path.isfile("/root/httpc2"):
        print("[*] Cronjob File Present")
        print("Check crontab -l To See If Script Set To Run On @reboot")
    else:
        f2 = open("/root/httpc2", "w")
        f2.write("@reboot /usr/bin/python3 /bin/httpc2/httpc2.py\n\n")
        f2.close()
        subprocess.call("crontab /root/httpc2", shell=True)
