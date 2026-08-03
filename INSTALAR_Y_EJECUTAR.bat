@echo off
cd /d "%~dp0"
if not exist entorno (
    py -m venv entorno
)
call entorno\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
pause
