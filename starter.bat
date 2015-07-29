@echo off
:loop 
   set /p action=Insert action: 
   python ttrack.py %action%
   goto loop
   
   