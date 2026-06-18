@echo off
title Local AI Engineer Setup
echo ====================================
echo   Local AI Engineer - Setup
echo ====================================
echo.

echo [1/4] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install Python 3.10+ from https://python.org
    pause
    exit /b 1
)
echo Python found.

echo [2/4] Installing backend dependencies...
cd /d "%~dp0backend"
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: pip install failed.
    pause
    exit /b 1
)
echo.

echo [3/4] Installing frontend dependencies...
cd /d "%~dp0frontend"
npm install
if %errorlevel% neq 0 (
    echo ERROR: npm install failed.
    pause
    exit /b 1
)
echo.

echo [4/4] Setup complete!
echo.
echo ====================================
echo   How to run:
echo.
echo   1. Start Ollama (if not running):
echo      ollama serve
echo.
echo   2. Pull a model (first time):
echo      ollama pull qwen2.5:7b
echo.
echo   3. Start backend (in one terminal):
echo      cd backend
echo      uvicorn app.main:app --reload
echo.
echo   4. Start frontend (in another terminal):
echo      cd frontend
echo      npm run dev
echo.
echo   5. Open http://localhost:5173
echo ====================================
pause
