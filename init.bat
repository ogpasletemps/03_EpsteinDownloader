@echo off
call python -m venv "03_EpsteinDownloader"
cd /d %~dp0/03_EpsteinDownloader/Scripts
call activate
cd /d %~dp0/
echo
call pip install -r requirements.txt