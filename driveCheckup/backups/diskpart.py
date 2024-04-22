#!/usr/bin/python3
"""Diskpart Test

Check the status of each drive and save output to logfile.

Requirements: Run as admin

Author: Dimitri Mojsejenko
"""
import os
import subprocess

def parseDiskpart(diskpartOutput):
    diskpartList = [s for s in diskpartOutput.splitlines(True) if s.strip()]
    indices = []
    summ = ""
    for i, line in enumerate(diskpartList):
        if "is now the selected disk." in line:
            indices.append(i+1)
            indices.append(i+3)
            indices.append(i+4)
        if "Volume" in line:
            indices.append(i)
        if "----------  ---  -----------  -----  ----------  -------  ---------  --------" in line:
            indices.append(i)
    for i, line in enumerate(diskpartList):
        if i in indices:
            if i == indices[-1]:
                summ += line.rstrip()
            else:
                summ += line.rstrip()+'\n'
    return summ

def checkDiskpartResults(diskpartresults):
    drivesOkay = True
    for line in diskpartresults:
        if "Volume" in line and not "Healthy" in line:
            drivesOkay = False
    return drivesOkay

def diskpart():
    if not os.path.isfile(".\diskpartCmds.txt"):
        with open(".\diskpartCmds.txt", 'w') as commands:
            cmds = """sel dis 0
det dis
sel dis 1
det dis"""
            commands.write(cmds)
    diskpartResults = subprocess.run(['diskpart', '/s', '.\diskpartCmds.txt'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    results = parseDiskpart(diskpartResults)
    print(results)
    print(checkDiskpartResults(results))
    
if __name__ == "__main__":
    diskpart()