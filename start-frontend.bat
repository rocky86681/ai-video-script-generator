@echo off
setlocal
title AI Video Script Generator - Frontend

:: Set the frontend directory with quotes to handle special characters like &
set "FRONT_DIR=%~dp0frontend"

echo 🚀 Navigating to frontend...
cd /d "%FRONT_DIR%"

if not exist node_modules (
    echo 📦 node_modules not found. Installing dependencies...
    call npm install
)

echo ⚡ Launching Vite Dev Server...
:: Use node directly with the full path to vite.js to avoid CMD path bugs
node "%FRONT_DIR%\node_modules\vite\bin\vite.js"

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ Vite failed to start.
    echo Possible reasons:
    echo 1. Node.js is not installed.
    echo 2. Port 5173 is already in use.
    echo 3. Dependencies are corrupted (try deleting node_modules and running this again).
)
pause
