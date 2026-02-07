@echo off
call python -m venv "03_EpsteinDowloader"
cd /d %~dp0/03_EpsteinDowloader/Scripts
call activate
cd /d %~dp0/
echo
call pip install -r requirements.txt