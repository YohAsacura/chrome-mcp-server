@echo off
echo ================================
echo Chrome MCP Server - Starting...
echo ================================
echo.

REM Navigate to project root
cd /d "%~dp0.."

REM Check if dependencies are installed
python -c "import selenium" > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Dependencies not installed!
    echo.
    echo Run installation first:
    echo   scripts\install.bat
    echo.
    pause
    exit /b 1
)

echo [OK] Starting server...
echo.
echo Press Ctrl+C to stop the server
echo.

python src\server.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server stopped with error!
    pause
    exit /b 1
)
