import subprocess
import sys,os

def clientconfig():
    setupscriptpath = "/root/ClientSetup.py"
    launcherpath = "/usr/share/applications/ClientSetup.desktop"
    if not os.path.isfile(launcherpath):
        subprocess.call("cp configs/ClientSetup.desktop " + launcherpath, shell=True)
        print("[*] Launcher Created\n\n")
    else:
        print("[*] Launcher already exists.\n\n")
    if not os.path.isfile(setupscriptpath):
        subprocess.call("cp scripts/ClientSetup.py " + setupscriptpath, shell=True)
        print("[*] Client-side configuration script created.\n\n")
    else:
        print("[*] Client-side confguration script already exists.\n\n")
