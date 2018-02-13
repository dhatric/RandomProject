@echo off  

@echo off
cls

cd C:\Giridhar\Projects\python\Doodles\RandomProject\com\doodles\video

FOR /F "TOKENS=1* DELIMS= " %%A IN ('DATE/T') DO SET CDATE=%%B
FOR /F "TOKENS=1,2 eol=/ DELIMS=/ " %%A IN ('DATE/T') DO SET mm=%%B
FOR /F "TOKENS=1,2 DELIMS=/ eol=/" %%A IN ('echo %CDATE%') DO SET dd=%%B
FOR /F "TOKENS=2,3 DELIMS=/ " %%A IN ('echo %CDATE%') DO SET yyyy=%%B

echo Time format = %time%

SET Timestamp=%dd%-%mm%-%yyyy%-%time:~0,2%-%time:~3,2%-%time:~6,2%

set pylogPath="C:\Giridhar\Projects\python\Doodles\RandomProject\com\doodles\output\logs\%Timestamp%.txt"

set pyexePath="C:\Python27\python.exe"  
set pronunciation_pyPath="C:\Giridhar\Projects\python\Doodles\RandomProject\com\doodles\video\DoodleChangeTracker.py" 


echo Start time: %date% %time% > %pylogPath%
%pyexePath% %pronunciation_pyPath% >> %pylogPath%
echo End time: %date% %time% >> %pylogPath%

