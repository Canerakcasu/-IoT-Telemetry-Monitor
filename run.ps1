# IoT Telemetry Monitor - PowerShell Run Script

$ProjectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectPath

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  IoT Telemetry Monitor" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Define venv Python path
$VenvPython = "$ProjectPath\.venv\Scripts\python.exe"

# Check if Python exists
if (!(Test-Path $VenvPython)) {
    Write-Host "Error: Virtual environment not found at $VenvPython" -ForegroundColor Red
    exit 1
}

Write-Host "Virtual Environment: $VenvPython" -ForegroundColor Yellow
Write-Host "Starting Flask server on http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run Flask app
& $VenvPython app.py
