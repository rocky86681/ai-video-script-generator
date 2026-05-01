@echo off
setlocal
echo ⚙️ Starting Backend API...
cd /d "%~dp0backend"

echo 🔍 Checking dependencies...
python -m pip install -r requirements.txt

echo 🚀 Launching FastAPI server...
python main.py
pause
