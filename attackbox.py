import subprocess
import sys,os
#import argparse


print('''

   ___         ________                 ____                 _ __
  / _ \___ ___/ /_  __/__ ___ ___ _    / __/__ ______ ______(_) /___ __
 / , _/ -_) _  / / / / -_) _ `/  ' \  _\ \/ -_) __/ // / __/ / __/ // /
/_/|_|\__/\_,_/ /_/  \__/\_,_/_/_/_/ /___/\__/\__/\_,_/_/ /_/\__/\_, /
                                                                /___/

Internal Pentest and Remote Wireless Testing Dropbox Installation Script
''')

if not os.geteuid() == 0:
    sys.exit("[!] Must Be Run As Root!")

print("Before Continuing Make Sure That DNS is Set for Remote Server and SSH Access Has Been Established (Needed for Transferring SSH Keys)")
input("Press ENTER to Continue")
print("\n")

#argument structure



## TODO:
# Install additional requested software
# Polling webserver Functionality
# automate SSH configuration
# RPi module
