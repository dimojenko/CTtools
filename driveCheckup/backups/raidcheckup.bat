@echo off
::Raid Checkup
::needs to be run as admin
set month=%date:~4,2%
set day=%date:~7,2%
set outfile=raidstatus_%month%_%day%.txt
type nul > %outfile%
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ >> %outfile%
echo                Drive Status                >> %outfile%
echo     Command: wmic diskdrive get model,name,serialnumber,status >> %outfile%
echo.>> %outfile%
wmic /append:%outfile% diskdrive get model,name,serialnumber,status
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ >> %outfile%
echo             Failure Prediction             >> %outfile%
echo     Command: wmic /namespace:\\root\wmi path MSStorageDriver_FailurePredictStatus >> %outfile%
echo.>> %outfile%
wmic /append:%outfile% /namespace:\\root\wmi path MSStorageDriver_FailurePredictStatus