#!/bin/bash

while true; do
	if ping -c 1 google.com &> /dev/null 
	then
		echo "Internet Up"
	else
		echo "Internet Down - Killing Wifi"
		ifconfig wlan0 down
		ifconfig wlan1 down
		ifconfig wlan2 down
		ifconfig eth0 down
		ifconfig eth0 up
	fi
	sleep 30
done
