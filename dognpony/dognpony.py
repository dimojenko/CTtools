#!/usr/bin/python3
"""Dog 'n Pony Show

Prepares desktop for a tour or open house. Opens various images from the Tours 
folder and sets window sizes and locations. The first time it is ran, window 
configurations are saved to currentDesktop.txt in the same location this code 
is ran. Then each subsequent run will open up the saved desktop configuration, 
if currentDesktop.txt exists. If you'd like to update the saved desktop 
configuration, simply delete any currentDesktop.txt in the run path and rerun.

Requirements: 
    * Run in Windows shell
    * Save files to display in "D:\5 - Tours\000000 OPEN HOUSE YO 000000\"

Author: Dimitri Mojsejenko
"""
import os
import time
import win32gui

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getWindows(hwnd, winList):
    """Gathers open windows and appends their titles, id, and dimensions to a given list."""
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if window_title and right-left and bottom-top:
            winList.append('{}, {}, [{},{},{},{}]'.format(window_title,hwnd,left,top,right,bottom))
    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def saveWindows():
    """Saves open window info to a text file."""
    win_list = []
    win32gui.EnumWindows(getWindows, win_list)  # gather list of open windows
    with open(r'.\currentDesktop.txt', 'w', encoding='utf-8') as curDesktop:
        for window in win_list:
            print(window, file=curDesktop)
            #curDesktop.write('%s\n' %window)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def findFile(name):
    fpath = False
    for root, dirs, files in os.walk("D:\\5 - Tours\\000000 OPEN HOUSE YO 000000"):
        if name in files:
            fpath = os.path.join(root, name)
    return fpath

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def displayWindows():
    with open(r'.\currentDesktop.txt', 'r') as curDesktop:
        for window in curDesktop:
            if ".jpg" in window:
                windowName = window.split('.jpg')[0]+'.jpg'
                windowLoc = window.split(', ')[2]
                windowPath = findFile(windowName)
                if windowPath:
                    os.startfile(windowPath)
            if ".nsihdr" in window:
                windowName = window.split('.nsihdr')[0]+'.nsihdr'
                windowName = windowName.split(' - ')[1]
                windowLoc = window.split(', ')[2]
                windowPathRoot = window.split(', ')[0].split(' (')[1].split(')')[0]
                windowPath = windowPathRoot+'\\'+windowName
                os.startfile(windowPath)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def moveWindows():
    savedWindows = []
    with open(r'.\currentDesktop.txt', 'r') as curDesktop:
        for line in curDesktop:
            savedWindows.append(line)
    #print(savedWindows)
    time.sleep(30)
    openWindows = []
    win32gui.EnumWindows(getWindows, openWindows)
    #print(openWindows)
    for window in openWindows:
        if ".jpg" in window:
            #print(window)
            windowName = window.split('.jpg')[0]+'.jpg'
            windowHWND = window.split(', ')[1]
            #print(windowHWND)
            for savedWindow in savedWindows:
                if windowName in savedWindow:
                    windowLoc = savedWindow.split(', ')[2]
                    windowLoc = ''.join(c for c in windowLoc if c not in '[]\\n')
                    windowLoc = windowLoc.split(',')
                    #print(windowLoc)
                    windowMoved = win32gui.MoveWindow(windowHWND, int(windowLoc[0]), int(windowLoc[1]), int(windowLoc[2])-int(windowLoc[0]), int(windowLoc[3])-int(windowLoc[1]), True)
        if ".nsihdr" in window:
            #print(window)
            windowName = window.split('.nsihdr')[0]+'.nsihdr'
            if "Resampling" in windowName:
                windowName = windowName.rsplit('\\',1)[-1]
            else:
                windowName = windowName.split(' - ')[1]
            #print(windowName)
            windowHWND = window.split(', ')[1]
            #print(windowHWND)
            for savedWindow in savedWindows:
                if windowName in savedWindow:
                    if not "Resampling" in windowName:
                        windowLoc = savedWindow.split(', ')[2]
                        windowLoc = ''.join(c for c in windowLoc if c not in '[]\\n')
                        windowLoc = windowLoc.split(',')
                        #print(windowLoc)
                        windowMoved = win32gui.MoveWindow(windowHWND, int(windowLoc[0]), int(windowLoc[1]), int(windowLoc[2])-int(windowLoc[0]), int(windowLoc[3])-int(windowLoc[1]), True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    if os.path.isfile('.\currentDesktop.txt'):
        displayWindows()
        moveWindows()
    else:
        saveWindows()