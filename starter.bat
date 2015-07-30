@echo off
:loop 
   set /p action="ttrack> "
   python ttrack.py %action%
   goto loop
   
   