@echo off
cd /d "%~dp0"
if not exist entorno\Scripts\python.exe (
    echo Primero ejecuta INSTALAR_Y_EJECUTAR.bat
    pause
    exit /b 1
)
call entorno\Scripts\activate.bat
python main.py
