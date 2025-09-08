@echo off
echo Installing dependencies for URL Converter...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found, installing dependencies...
echo.

REM Install requirements
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error installing dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo You can now run the program with: python converter.py
echo Or build executable with: python build_exe.py
echo.
pause

