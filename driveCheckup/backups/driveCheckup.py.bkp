#!/usr/bin/python3
"""Drive Checkup

Check the status of each drive and save output to logfile.

Requirements: Run as admin

Author: Dimitri Mojsejenko
"""
import os
import sys
import win32gui
import subprocess
from datetime import datetime

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseCheckDisk(checkDiskOutput):
    checkDiskLines = checkDiskOutput.splitlines()
    problem = 0
    found = False
    for i, line in enumerate(checkDiskLines):
        if "problem" in line and not found:
            problem = i
            found = True
    summ = "\n".join(checkDiskLines[problem::])
    return summ
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseSpeedTest(speedTestOutput):
    indices = [16,17,18,20,21]
    summ = ""
    if "txt" in speedTestOutput:
        with open(speedTestOutput, 'r') as speedTestLines:
            for i, line in enumerate(speedTestLines):
                if i in indices:
                    summ += line[0:-4]
                    if not i == 21:
                        summ += '\n'
    else:
        speedTestLines = speedTestOutput.splitlines()
        for i, line in enumerate(speedTestLines):
                if i in indices:
                    summ += line[0:-4]
                    if not i == 21:
                        summ += '\n'
    return summ
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseFailPredict(failPredictOutput):
    failPredictLines = failPredictOutput.splitlines()
    indices = []
    summ = ""
    for i, line in enumerate(failPredictLines):
        if "Active" in line:
            indices.append(int(i))
    for index in indices:
        summ = "\n".join(failPredictLines[index:index+5])
        if not index == indices[-1]:
            summ += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        else:
            summ += "\n"
    return summ

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseDiskpart(diskpartOutput):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def checkDriveStatusResults(drivestatus):
    drivesOkay = True
    driveInfo = []
    for drive in drivestatus[1::]:
        info = drive.split("  ")
        driveInfo.append([s for s in info if s.strip()])
    for drive in driveInfo:
        if len(drive) > 2:
            if not drive[3].strip() == "OK":
                drivesOkay = False
    return drivesOkay
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def checkCheckDiskResults(parseCheckDiskResults):
    drivesOkay = True
    if not "No further action is required." in parseCheckDiskResults.splitlines()[1]:
        drivesOkay = False
    return drivesOkay
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
def checkFailPredictResults(parseFailPredictResults):
    drivesOkay = True
    for line in parseFailPredictResults.splitlines():
        if "PredictFailure" in line:
            if not "False" in line:
                drivesOkay = False
    return drivesOkay
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def checkDiskpartResults(diskpartresults):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def driveCheckup():
    driveStatusText = '''\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        DRIVE STATUS
    Command: wmic diskdrive get model,name,serialnumber,status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'''
    checkDiskCText = '''\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        CHECK DISKS
    Command: chkdsk C:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'''
    checkDiskDText = '''\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Command: chkdsk D:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'''
    speedtestCText = '''\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        SPEED TEST
    Command: winsat disk -drive C
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'''
    speedtestDText = '''\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Command: winsat disk -drive D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'''
    failPredictText = '''\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                     FAILURE PREDICTION
    Command: Get-WmiObject -namespace root\wmi -class MSStorageDriver_FailurePredictStatus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'''
    summary = '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    DRIVE CHECKUP SUMMARY\n'''  
    fullResults = '''\n\n\n\n\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                     FULL DRIVE CHECKUP
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n'''

    # Commands
    driveStatus = subprocess.run(['cmd.exe', '/c', 'wmic diskdrive get model,name,serialnumber,status'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    driveStatus = [s for s in driveStatus.splitlines(True) if s.strip()]
    driveStatusOutput = "".join(driveStatus)
    checkDiskC = subprocess.run(['cmd.exe', '/c', 'chkdsk C:'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    checkDiskD = subprocess.run(['cmd.exe', '/c', 'chkdsk D:'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    #speedtestC = subprocess.run(['cmd.exe', '/c', 'winsat disk -drive C'], stdout=subprocess.PIPE).stdout.read().strip()
    #speedtestD = subprocess.run(['cmd.exe', '/c', 'winsat disk -drive D'], stdout=subprocess.PIPE).stdout.read().strip()
    failPredict = subprocess.run(['powershell.exe', '/c', 'Get-WmiObject -namespace root\wmi -class MSStorageDriver_FailurePredictStatus'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    
    # Parse Output
    driveStatusSumm = driveStatusText + driveStatusOutput
    parseCheckDiskCoutput = parseCheckDisk(checkDiskC)
    checkDiskSumm = checkDiskCText + parseCheckDiskCoutput
    parseCheckDiskDoutput = parseCheckDisk(checkDiskD)
    checkDiskSumm += checkDiskDText + parseCheckDiskDoutput
    #speedtestSumm = speedtestCText + parseSpeedTest(speedtestC)
    #speedtestSumm += speedtestDText + parseSpeedTest(speedtestD)
    parseFailPredictOutput = parseFailPredict(failPredict)
    failPredictSumm = failPredictText + parseFailPredictOutput
    
    # Check results
    drivesOkay = checkDriveStatusResults(driveStatus) and checkFailPredictResults(parseFailPredictOutput)
    maybeOkay = checkCheckDiskResults(parseCheckDiskCoutput) and checkCheckDiskResults(parseCheckDiskDoutput)
    drivesHealthy = "                   All drives are healthy!\n"
    drivesProblem = "           Drives need attention! Check full log.\n"
    drivesMaybeOkay = "Drives are likely healthy. Check log if experiencing issues.\n"
    if drivesOkay:
        if maybeOkay:
            summary += drivesHealthy
        else:
            summary += drivesMaybeOkay
    else:
        summary += drivesProblem
    summaryClose = '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n'''
    summary += summaryClose
    
    # Assemble Output
    #summary += driveStatusSumm + checkDiskSumm + speedtestSumm + failPredictSumm
    summary += driveStatusSumm + checkDiskSumm + failPredictSumm
    #fullResults += driveStatusSumm+checkDiskCText+checkDiskC+checkDiskDText+checkDiskD+speedtestCText+speedtestC+speedtestDText+speedtestD+failPredictText+failPredict
    fullResults += driveStatusSumm+checkDiskCText+checkDiskC+checkDiskDText+checkDiskD+failPredictText+failPredict
    output = summary+fullResults
    
    # Remove progress lines from output
    cleanOutput = []
    for line in output.splitlines():
        if not "Progress:" in line:
            cleanOutput.append(line)
    cleanOutput = "\n".join(cleanOutput)
    
    # Get current date for logfile
    today = datetime.now()
    datestr = today.strftime('%m_%d')
    filename = "drivestatus_"+datestr+".txt"
    
    # Delete logfile if it already exists
    if os.path.exists("filename"):
        os.remove("filename")
    
    print(cleanOutput)
    # Write output to logfile
    with open(filename, 'w') as outfile:
        outfile.write(cleanOutput)

if __name__ == "__main__":
    driveCheckup()