
set "root=%~dp0"
set "file=file:///%~dp0dist/index.html?url=http://localhost:8082/api/rest/documentation"

start iexplore.exe %file%

rem start iexplore.exe "file:\\\d:\eWamSublimeAdaptor/dist/index.html?url=http://localhost:8082/api/rest/documentation"