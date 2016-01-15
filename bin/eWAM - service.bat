@call "%~dp0eWAM Set Env.bat"

@set WYDE-BINARY=64
set "PATH=%WYDE-ROOT%\WFDll\%WYDE-BINARY%;%WF-ROOT%\bin;%PATH%"


start ewamconsole.exe /RUNASSERVICE:(WYDE-ROOT)/bin/ewam.json %*
@exit /B