@echo off
setlocal

call :build_package "%1"

echo You may copy the desired package in SublimeText Package folder.
pause

goto :endofscript


:build_package
cd %1
del /F /Q ..\Gold.sublime-package
..\zip.exe -q ..\Gold.sublime-package *
cd ..
echo Created Gold.sublime-package.
GOTO:EOF

:endofscript
endlocal