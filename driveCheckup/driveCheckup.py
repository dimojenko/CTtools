#!/usr/bin/python3
"""Drive Checkup

Check the status of each drive and save output to logfile.

Requirements: Run as admin

Author: Dimitri Mojsejenko
"""
import os
import subprocess

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def checkDriveStatusResults(drivestatus):
    drivesOkay = True
    driveInfo = []
    for drive in drivestatus[1::]:
        info = drive.split("  ")
        driveInfo.append([s for s in info if s.strip()])
    for drive in driveInfo:
        if len(drive) > 2:
            if not drive[-1].strip() == "OK":
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
    drivesOkay = True
    for line in diskpartresults:
        if "Volume" in line and not "Healthy" in line and not "---" in line:
            drivesOkay = False
    return drivesOkay

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def driveCheckup():
    driveStatusText = '''\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        DRIVE STATUS
    Command: wmic diskdrive get model,name,serialnumber,status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'''
    diskpartText = '''\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                         DISKPART
    Command: diskpart; sel dis 0; det dis; sel dis 1; det dis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'''
    checkDiskCText = '''\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        CHECK DISKS
    Command: chkdsk C:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'''
    checkDiskDText = '''\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Command: chkdsk D:
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

    # Create diskpart commands if not available
    if not os.path.isfile(".\diskpartCmds.txt"):
        dpcmds = """sel dis 0
det dis
sel dis 1
det dis"""
        with open(".\diskpartCmds.txt") as diskpartCmds:
            diskpartCmds.write(dpcmds)

    # Commands
    driveStatus = subprocess.run(['cmd.exe', '/c', 'wmic diskdrive get model,name,serialnumber,status'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    driveStatus = [s for s in driveStatus.splitlines(True) if s.strip()]
    driveStatusOutput = "".join(driveStatus)
    diskpart = subprocess.run(['diskpart', '/s', 'diskpartCmds.txt'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    checkDiskC = subprocess.run(['cmd.exe', '/c', 'chkdsk C:'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    checkDiskD = subprocess.run(['cmd.exe', '/c', 'chkdsk D:'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    failPredict = subprocess.run(['powershell.exe', '/c', 'Get-WmiObject -namespace root\wmi -class MSStorageDriver_FailurePredictStatus'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    
    # Parse Output
    driveStatusSumm = driveStatusText + driveStatusOutput
    diskpartSumm = diskpartText + parseDiskpart(diskpart)
    parseCheckDiskCoutput = parseCheckDisk(checkDiskC)
    checkDiskSumm = checkDiskCText + parseCheckDiskCoutput
    parseCheckDiskDoutput = parseCheckDisk(checkDiskD)
    checkDiskSumm += checkDiskDText + parseCheckDiskDoutput
    parseFailPredictOutput = parseFailPredict(failPredict)
    failPredictSumm = failPredictText + parseFailPredictOutput
    
    # Check results
    drivesOkay = checkDriveStatusResults(driveStatus) and checkFailPredictResults(parseFailPredictOutput) and checkDiskpartResults(diskpartSumm)
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
    summary += driveStatusSumm + diskpartSumm + checkDiskSumm + failPredictSumm
    fullResults += driveStatusSumm+diskpartText+diskpart+checkDiskCText+checkDiskC+checkDiskDText+checkDiskD+failPredictText+failPredict
    output = summary+fullResults
    
    # Remove progress lines from output
    cleanOutput = []
    for line in output.splitlines():
        if not "Progress:" in line:
            cleanOutput.append(line)
    cleanOutput = "\n".join(cleanOutput)
    
    # Print output to logfile in driveCheckup.bat
    print(cleanOutput)

if __name__ == "__main__":
    driveCheckup()