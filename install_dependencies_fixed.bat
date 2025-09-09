@echo off
echo ========================================
echo  URL Converter - Dependency Installer
echo ========================================
echo.

echo [1/4] Python version check...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo.
echo [2/4] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [3/4] Installing/updating dependencies...
python -m pip install --upgrade -r requirements.txt

echo.
echo [4/4] Verifying installation...
python -c "import yt_dlp, ssl, certifi, requests; print('All dependencies installed successfully!')"

if %errorlevel% neq 0 (
    echo ERROR: Some dependencies failed to install.
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Installation completed successfully!
echo ========================================
echo.
echo You can now run the program with:
echo   python converter.py
echo.
echo Or create an executable with:
echo   python build_exe.py
echo.
pause
