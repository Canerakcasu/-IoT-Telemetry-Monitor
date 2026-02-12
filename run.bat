@echo off
REM IoT Telemetry Monitor - Run Script
REM This script runs the Flask application using the virtual environment

echo Starting IoT Telemetry Monitor...
cd /d "%~dp0"

REM Use relative path to venv Python (assuming .venv is in the same root)
"%~dp0.venv\Scripts\python.exe" app.py

pause
