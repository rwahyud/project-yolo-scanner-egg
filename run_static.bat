@echo off
cls
echo.
echo ========================================
echo    EGG COUNTING - STATIC MODE
echo ========================================
echo.
echo Hitung telur yang terlihat di layar:
echo - 4 telur visible = count 4
echo - 0 telur visible = count 0
echo.
echo Tekan Q untuk quit
echo.

cd /d "%~dp0"

.\venv\Scripts\python.exe egg_counting_static.py

pause
