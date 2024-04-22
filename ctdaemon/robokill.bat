@echo off
::taskkill /f /pid %%I
for /f "tokens=2 delims= " %%I in ('tasklist ^| findstr /i "robocopy"') do (
	taskkill /f /pid %%I
)