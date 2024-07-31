@echo off
REM Change directory to the script's location
cd /d "%~dp0"

REM Activate your Python environment if necessary
REM call path\to\your\venv\Scripts\activate.bat

REM Start the backend script
start python apptracker_main.py --sleep_time 1 --port 5000

REM Start the frontend script using npm
start npm run dev

REM Optional: Wait for both processes to end
REM wait
