# CTtools
- tools for assisting with various tasks in the CT lab

___
## CT Daemon
This is a GUI allowing one to transfer scan data from an aquisition machine to one of the 
other machines in the lab during scanning. Once the source and destination have been selected, 
hitting "Start ROBOCOP" will begin the file transfer. The transfer process will continue for 
one day, if not killed with the "Kill all jobs" button. There is no problem with letting a 
transfer process continue after files are done transferring; the process will simply be killed 
after one day has elapsed. Multiple transfers can be working at the same time, so there is no 
issue with starting multiple transfers without killing one. 
Everything except ".nsipro" files will be transferred.
Occasionally a transfer will fail to move all files or seem to pause for no reason. Most of 
the time, simply hitting the "Kill all jobs" button, and restarting the transfer will fix it. 
In the GUI, there is also a "Scan Notifier" button, which when pressed, will send a message to 
the "Scan Notifications" channel in the "RDL CT Team" MS Teams page. 
Logs for each file transfer process are stored in the "robocopy_logs" folder, named according 
to the start time. 

## Drive Checkup 
This is a script which will run various drive checks and log the results in order to keep track 
of the health of the data drives throughout the lab. This is intended to be setup as a scheduled 
task in MS Task Scheduler to be run each night. Another script set as a later scheduled task will 
parse the results and send an email notification if there's any concerns. 

## Dog n' Pony
This script allows one to quickly setup one's desktop with a saved window configuration of 
scans and images for showing tours. When first run, it will save the window information of 
the currently open windows, if they are either ".nsipro" or image files; this info is saved 
as "currentDesktop.txt". When run while "currentDesktop.txt" is already created and in the run 
directory, all the previously saved windows will be opened in their saved locations.

## Mouse Mover
This script is intended to be used to prevent any screen savers or locks from interferring with 
something such as a Box data upload. When run, the mouse will make random movements around the 
screen to simulate activity.
