import subprocess
import sys,os

#This script allows the client-side modification of the autossh server and port setting if required.

def ClientSetup():
    if os.path.isfile("/root/reverse.sh"):
        #backup old configuration
        if not os.path.isfile("/root/reverse.sh.bak"):
            subprocess.call("cp /root/reverse.sh /root/reverse.sh.bak", shell=True)
    
        #Set new server and port number
        while True:
            server1 = input("Please enter the fully qualified domain name or IP address:\n")
            server2 = input("Please retype the fully qualified domain name or IP address:\n")
            if server1 != server2:
                print("The domain names or IP addresses do not match.")
                continue
            port1 = input("Please enter the port number:\n")
            port2 = input("Please retype the port number:\n")
            if port1.isnumeric():
                if port1 == port2:
                    if int(port1) > 1024 and int(port1) <= 65535:
                        rev_ssh = '/usr/bin/autossh -M 0 -f -N -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -R ' + port1 + ':localhost:22 autossh@' + server1
                        f = open("/root/reverse.sh", "w")
                        f.write("#!/bin/bash")
                        f.write("\n\n")
                        f.write(rev_ssh)
                        f.close()
                        subprocess.call("/usr/sbin/reboot", shell=True)
                        break
                    else:
                        print("Port number out of range. Please try again.")
                else:
                    print("The port numbers entered do not match.")
            else:
                print("Invalid port number. Please try again.")
    else:
        print("Error: /root/reverse.sh does not exist.")
ClientSetup()
