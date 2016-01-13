@call "%~dp0eWAM Set Env.bat"
start ewamconsole.exe /RUNASSERVICE:(WYDE-ROOT)/bin/ewam.json %*
@exit /B