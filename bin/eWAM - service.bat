@call "%~dp0eWAM Set Env.bat"
start ewam.exe /RUNASSERVICE:(WYDE-ROOT)/bin/ewam.json %*
@exit /B