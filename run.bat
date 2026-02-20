@echo off
cd /d %~dp0/03_EpsteinDownloader/Scripts
call activate
cd /d %~dp0/
echo
call curl http://artscene.textfiles.com/asciiart/cubes

:start
set /p user_input= Moteur de recherche / Telechargement en batch (0/1) ?:
if not defined user_input goto start
if /i %user_input%==0 goto zero
if /i %user_input%==1 (goto one) else (goto invalid)

:zero
call moteur_de_recherche.py
pause
exit

:one
call telechargement_batch.py
pause
exit

:invalid
echo [X] Mauvaise saisie pour le choix de telechargement. Veuillez reessayer.
goto start