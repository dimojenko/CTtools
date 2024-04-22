@echo off
cd /D "%~dp0"
set mmdd=%date:~4,2%_%date:~7,2%
set logfile="D:driveCheckupLogs\O\driveStatus_O_%mmdd%.txt"
"C:\Users\efX-user\AppData\Local\Microsoft\WindowsApps\python.exe" "C:\Users\efX-user\Documents\driveCheckup\driveCheckup.py" > %logfile%