@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python to run this game.
    pause
    exit /b
)

REM Check if loguru is installed
python -c "import loguru" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Installing required Python packages...
    pip install -r requirements.txt
)

REM Run the game
python game.py
pause
