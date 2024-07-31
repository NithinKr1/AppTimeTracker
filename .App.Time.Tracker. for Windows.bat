@echo off
REM Change directory to the script's location
cd /d "%~dp0"

REM Activate your Python environment if necessary
REM call path\to\your\venv\Scripts\activate.bat

REM Start the backend script
start pythonw apptracker_main.py --sleep_time 1 --port 5000

REM wait
