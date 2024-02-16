#!/usr/bin/python3
"""Scan Demon

This script looks through open windows to find if there's a scan completion notification.
When one is found, the team is notified through Microsoft Teams chat.

Author: Dimitri Mojsejenko
"""
import win32gui
import pymsteams
from tkinter import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def buttonHandler(but, msg):
    """Sends MS Teams message and modifies GUI message when button is pressed."""
    if (but['state'] == 'normal'):
        but['state'] = 'disabled'
        msg.set("running...")
        sendTeamsMsg()

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    #GUI
    root = Tk()
    # set GUI window width and height
    w = 300
    h = 100
    # set GUI window location (top-left = 0,0)
    x = 500
    y = 1200
    root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # (<width>x<height>+<x>+<y>)
    root.title("Scan Demon")

    # Button
    row1 = Frame(root)
    messageText = StringVar(root)
    scanBut = Button(row1, text="Monitor Scan", height=2, width=13)
    scanBut.bind('<Button>', lambda sButHandler: buttonHandler(scanBut, messageText))
    scanBut.pack() 
    row1.pack(side=TOP, fill=X, padx=5, pady=5)

    # GUI message
    message = Label(textvariable=messageText)
    message.pack(side=BOTTOM)

    # needed to continuously run sendTeamsMsg() to check for open windows
    root.after(0, sendTeamsMsg())

    root.mainloop()