@echo off
REM Quick start script for Classroom Manager with Network Support

echo.
echo 🎓 Classroom Manager - Network Setup Script
echo ==========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed
    exit /b 1
)

for /f "tokens=*" %%A in ('python --version') do set PYTHON_VERSION=%%A
echo ✅ Python found: %PYTHON_VERSION%

REM Navigate to project directory
cd /d "%~dp0lab_manager"

echo.
echo 📦 Installing dependencies...
python -m pip install -r requirements.txt -q

echo.
echo ✅ Dependencies installed
echo.
echo ==========================================
echo Setup Options:
echo.
echo 1) Start Server (GUI) - Recommended
echo    python -m server.gui.main_window
echo.
echo 2) Start Agent on Workstation
echo    python -m agent.main
echo.
echo 3) Test Network Discovery
echo    python -c "from server.network_discovery import discover_agents_sync; print(discover_agents_sync())"
echo.
echo ==========================================
echo.
echo For detailed setup instructions, see:
echo   - NETWORK_SETUP_RU.md (Russian)
echo   - NETWORK_SETUP_EN.md (English)
echo.
pause

