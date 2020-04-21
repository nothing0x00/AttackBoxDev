# Holding area for script to grab commands from webserver, parse commands and run
# Will need functionality in install scripts to set this script to run as a cronjob every 2 minutes
# Use prompt in install script to set domain name for this script (which needs to run headless)
# Use requests to reach out to grab file, parse the file, diff it against the last version and run each command, line by line
