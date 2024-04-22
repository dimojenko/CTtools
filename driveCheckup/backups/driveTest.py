#!/usr/bin/python3
"""Drive Checkup Test

Check the status of each drive and save output to logfile.

Requirements: Run as admin

Author: Dimitri Mojsejenko
"""
import os
import sys
import win32gui
import subprocess
from datetime import datetime

def driveCheckup():
    #with open("speedtest1.txt", 'w') as speedtest1text:
    #    speedtest1 = subprocess.run(['powershell.exe', '/c', 'winsat disk -drive C'], stdout=speedtest1text, text=True)
    #    print(speedtest1)
    #speedtest2 = subprocess.run(['powershell.exe', '/c', 'winsat disk -drive C'], stdout=subprocess.PIPE).stdout.decode().strip()
    #print(speedtest2)
    speedtest2 = subprocess.Popen(['cmd.exe', '/c', 'winsat disk -drive C'], stdout=subprocess.PIPE)
    #speedtest2output = subprocess.check_output(('cmd.exe', '/c', 'winsat disk -drive C'), stdin=speedtest2.stdout)
    try:
        output, errs = speedtest2.communicate(timeout=15)
    except TimeoutExpired:
        output, errs = speedtest2.communicate()
    print(output)
    print(errs)
    #speedtest4 = subprocess.run(['powershell.exe', '/c', 'winsat disk -drive C'], capture_output=True)
	#print(speedtest4.stdout.read().strip())

if __name__ == "__main__":
    driveCheckup()