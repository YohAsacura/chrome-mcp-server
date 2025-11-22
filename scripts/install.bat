@echo off
echo ================================
echo Chrome MCP Server - Installation
echo ================================
echo.

REM Navigate to project root
cd /d "%~dp0.."

REM Check Python version
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed!
    pause
    exit /b 1
)

echo.
echo ================================
echo [SUCCESS] Installation complete!
echo ================================
echo.
echo To start the server:
echo   scripts\start.bat
echo.
echo Or manually:
echo   python src\server.py
echo.
pause
