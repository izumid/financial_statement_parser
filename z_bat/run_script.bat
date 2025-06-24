@echo off
TITLE RUN PROG: 

set "path_env=%~dp0\venv\Scripts"
echo Enviroment path: %path_env%

call "%path_env%\activate.bat"
call "%path_env%\python.exe" "%~dp0main.py" /popup
call "%path_env%\deactivate.bat"

pause