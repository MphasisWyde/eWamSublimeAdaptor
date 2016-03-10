@echo off
setlocal

call :build_package "%1"

echo You may copy the desired package in SublimeText Package folder.
pause

goto :endofscript


:build_package
cd ..\src
del /F /Q ..\release\Gold.sublime-package
..\build\zip.exe -r -q ..\release\Gold.sublime-package *
cd ..
echo Created Gold.sublime-package.
GOTO:EOF

:endofscript
endlocal