@ECHO OFF

rem temp add
Timeout /T 2 /Nobreak

:LOOP
tasklist | find /i "kodi" >nul 2>&1
IF ERRORLEVEL 1 (
  GOTO CONTINUE
) ELSE (
  ECHO Kodi is still running
  Timeout /T 2 /Nobreak
  GOTO LOOP
)

:CONTINUE
rem Timeout /T 2 /Nobreak
