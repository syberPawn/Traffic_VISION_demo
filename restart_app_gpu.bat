@echo off
cd /d "%~dp0"
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8501" ^| findstr "LISTENING"') do taskkill /PID %%p /F >nul 2>nul
call .venv\Scripts\activate.bat
python -m streamlit run app.py --server.port 8501
