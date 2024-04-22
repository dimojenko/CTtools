#!/usr/bin/python3
"""Drive Check Notifier

Parse logfiles of drive checks and email results as needed.

Requirements: Run as admin

Author: Dimitri Mojsejenko
"""
import os
import subprocess
import yagmail
import datetime

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parseLogfiles():
    today = datetime.datetime.now()
    date = str(today.month)+"_"+str(today.day)
    logfiles = []
    
    for root, dirs, files in os.walk("D:\driveCheckupLogs"):
        for file in files:
            if date in file:
                fpath = os.path.join(root, file)
                with open(fpath, 'r') as logfile:
                    loglines = logfile.readlines()
                    result = loglines[3]
                    if "attention" in result:
                        logfiles.append(str(fpath))
    return logfiles

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def sendEmail(logfiles):
    openFiles = []
    for file in logfiles:
        f = open(file, 'r')
        openFiles.append(f)
    
    drives = []
    for log in logfiles:
        drives.append(log.split('\\')[2])
    drives = ", ".join(drives)
    
    receiver = "wmojseje@its.jnj.com"
    body = "One or more drives need attention on {drive}. Check attached log.".format(drive=drives)
    
    yag = yagmail.SMTP("ctethicon@gmail.com", "dccc snhn tgsq rgqv")
    
    yag.send(
        to = receiver,
        subject = "Drive Checkup",
        contents = body,
        attachments = openFiles
    )
    
if __name__ == "__main__":
    badDriveLogs = parseLogfiles()
    sendEmail(badDriveLogs)