#!/usr/bin/python3
"""CT Daemon

A GUI that allows one to copy data during scans with an option for an MS Teams 
notification when the current scan is done. 

* Everything except the .nsipro files will be copied

* If the source project folder already exists at the destination, do not include the 
project folder in the destination path; if it is included, then a copy of the 
project folder will be created within the project folder at the destination. 

* If the source project folder doesn't exist at the destination, it will be created.

Requirements: Run in Windows shell, since Windows style paths are used.

Author: Dimitri Mojsejenko
"""
import os
import sys
import win32gui
import pymsteams
import subprocess
from tkinter import *
from tkinter.filedialog import askdirectory
from datetime import datetime, timedelta

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getUser():
    """Gets the current user of the machine."""
    user = subprocess.run(['cmd.exe', '/c', 'echo %USERNAME%'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    return user

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def chooseDir(tkEntry, msg):
    """Opens user dialogue asking for directory, and stores name into given Tkinter entry."""
    initialDir = 'D:\\'
    fname = askdirectory(initialdir=initialDir, mustexist=True)
    tkEntry.delete(0,END)
    tkEntry.insert(0,fname) # display selected directory
    msg.set("")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def robocop(src, dst, msg):
    """Starts a robocopy job with given source and dest dirs."""
    with open('ROBOCOPJOBtemplate.RCJ', 'r') as jobTemplate:
        jobfile = jobTemplate.readlines()
    
    # Add source folder to destination paths
    folder = src.split('/')[-1]
    if not folder in dst:
        dst = dst+'/'+folder
    
    # Add source and destination to jobfile
    jobfile[4] = "\t/SD:"+src
    jobfile[9] = "\t/DD:"+dst

    # Get current user and time to add to logfile
    today = datetime.now()
    curTime = today.strftime('%H%M')
    user = getUser()
    logfile = "\t/LOG+:C:\\Users\\"+user+"\\Documents\\robocopy_logs\\robocopy_log"+curTime+".txt"
    jobfile[-1] = logfile
    
    # convert list to string
    jobfile = ''.join(jobfile)
    
    # Write new jobfile
    with open('ROBOCOPJOB.RCJ', 'w') as robocopJob:
        robocopJob.write(jobfile)

    # Run robocopy job
    cmd = "robocopy /job:robocopjob.rcj"
    subprocess.Popen(['powershell.exe', cmd]) # 'Popen' instead of 'run' doesn't wait for process to finish
    msg.set("Robocop on patrol...")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def killJobs(msg):
    """Kills all active robocopy jobs."""
    subprocess.run("robokill.bat")
    msg.set("Jobs killed. Robocop off duty.")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def buttonHandler(but, msg):
    """Sends MS Teams message and modifies GUI message when button is pressed."""
    if (but['state'] == 'normal'):
        but['bg'] = 'deep sky blue'
        but['disabledforeground'] = 'snow'
        but['state'] = 'disabled'
        msg.set("Monitoring scan...")
        sendTeamsMsg()
    else:
        but['state'] = 'normal'
        but['bg'] = 'SystemButtonFace' # default color
        msg.set("")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getWindows(hwnd, strings):
    """Gathers open windows and appends their titles to the supplied list."""
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if window_title and right-left and bottom-top:
            strings.append('{}'.format(window_title))
    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def sendTeamsMsg():
    """Sends MS Teams message when scan is done."""
    if (scanBut['state'] == 'disabled'):
        win_list = []  # list of strings containing win handles and window titles
        win32gui.EnumWindows(getWindows, win_list)  # gather list of open windows
        
        # Connector Card created from MS Teams
        teamsMessage = pymsteams.connectorcard("https://jnj.webhook.office.com/webhookb2/563203bf-bdc7-4796-867e-113f1f63140f@3ac94b33-9135-4821-9502-eafda6592a35/IncomingWebhook/772e0ec4f0ed4ae79ed97e4706f2846b/d9af7180-7f63-4448-b4e6-104d2b044ecb")
        teamsMessage.text("Scan Completed")

        for window in win_list:  # parse results for particular window title
            if window == "Scan Done...":
                teamsMessage.send()
                messageText.set("")
                scanBut['state'] = 'normal'
    # repeat every second
    root.after(1000, sendTeamsMsg)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    root = Tk()

    # Source
    robocopMsg = StringVar(root)
    row1 = Frame(root)
    sourceLabel = Label(row1, width=18, text="Source Directory:", anchor='w')
    sourceDir = StringVar()
    sourceEntry = Entry(row1, textvariable=sourceDir)
    sourceBut = Button(row1, text="Choose Source", width=15)
    sourceBut.bind('<Button>', lambda fButHandler: chooseDir(sourceEntry, robocopMsg))
    row1.pack(side=TOP, fill=X, padx=5, pady=5)
    sourceLabel.pack(side=LEFT)
    sourceEntry.pack(side=LEFT, expand=YES, fill=X)
    sourceBut.pack(side=RIGHT)
    
    # Destination
    row2 = Frame(root)
    destLabel = Label(row2, width=18, text="Destination Directory:", anchor='w')
    destDir = StringVar()
    destEntry = Entry(row2, textvariable=destDir)
    destBut = Button(row2, text="Choose Destination", width=15)
    destBut.bind('<Button>', lambda fButHandler: chooseDir(destEntry, robocopMsg))
    row2.pack(side=TOP, fill=X, padx=5, pady=5)
    destLabel.pack(side=LEFT)
    destEntry.pack(side=LEFT, expand=YES, fill=X)
    destBut.pack(side=RIGHT)

    # Start and Kill Buttons
    row3 = Frame(root)
    copyFrame = Frame(row3, highlightbackground="chartreuse3", highlightthickness=2, bd=0)
    copyBut = Button(copyFrame, text="Start ROBOCOP", height=2, width=13)
    copyBut.bind('<Button>', lambda sButHandler: robocop(sourceDir.get(), destDir.get(), robocopMsg))
    copyBut.pack()
    copyFrame.pack(side=LEFT, padx=(50,30))
    killFrame = Frame(row3, highlightbackground="red3", highlightthickness=2, bd=0)
    killBut = Button(killFrame, text="Kill all jobs", height=2, width=13)
    killBut.bind('<Button>', lambda sButHandler: killJobs(robocopMsg))
    killBut.pack()
    killFrame.pack(side=LEFT, padx=(0,50))
    
    # ScanDemon Button
    scanDemonMsg = StringVar(root)
    scanDemonFrame = Frame(row3, highlightbackground="deep sky blue", highlightthickness=2, bd=0)
    scanBut = Button(scanDemonFrame, text="Scan Notifier", height=2, width=13)
    scanBut.bind('<Button>', lambda sButHandler: buttonHandler(scanBut, scanDemonMsg))
    scanBut.pack()
    scanDemonFrame.pack(side=RIGHT, padx=(0,100))
    row3.pack(side=TOP, fill=X, pady=20)
    
    # GUI messages
    messageRow = Frame(root)
    robocopMessage = Label(messageRow, textvariable=robocopMsg)
    robocopMessage.pack(side=LEFT, padx=50)
    scanDemonMessage = Label(messageRow, textvariable=scanDemonMsg)
    scanDemonMessage.pack(side=RIGHT, padx=100)
    messageRow.pack(side=BOTTOM, fill=X, pady=(0,8))

    # set GUI window width and height
    w = 600
    h = 180
    # set GUI window location (top-left = 0,0); dependent on individual dual screen setup
    x = 300
    y = 800
    root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # (<width>x<height>+<x>+<y>)
    root.minsize(w,h)
    root.maxsize(w,h) # setting minsize = maxsize makes GUI window constant size
    root.title("CT Daemon")
    icon = PhotoImage(file="logo_symbol.png")
    root.iconphoto(False, icon)
    
    # needed to continuously run sendTeamsMsg() to check for open windows
    root.after(0, sendTeamsMsg())
    
    root.mainloop()