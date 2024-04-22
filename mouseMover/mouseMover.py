#!/usr/bin/python3
"""Mouse Mover

Moves the mouse every few minutes to prevent lock screen.

Author: Dimitri Mojsejenko
"""
import time
import pyautogui

def main():
    pos = "zero"
    while True:
        if pos == "zero":
            pyautogui.moveTo(0, 0, duration = 1)
            pos = "moved"
        else:
            pyautogui.moveTo(0, 10, duration = 1)
            pos = "zero"
        time.sleep(60)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    main()