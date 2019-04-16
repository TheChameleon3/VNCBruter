# VNCBruter

VNC pentest tool with bruteforce and ducky script execution features

VNCBruter is a VNC pentest tool writen in Python
Written by Jason Spencer

It is based off of VNC.py written by Hegusung

Starting vncserver 
vnc4server :1 -blacklistthreshold 10000

Example uses
python3 ./vncbrute.py -p 5901 -P password.txt -l 127.0.0.2 -O vnc
python3 ./vncbrute.py -P password.txt -lL targets.txt
