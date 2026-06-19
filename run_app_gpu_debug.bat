@echo off
cd /d "%~dp0"
if not exist tmp mkdir tmp
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8501" ^| findstr "LISTENING"') do taskkill /PID %%p /F >nul 2>nul
call .venv\Scripts\activate.bat
python -m streamlit run app.py --server.port 8501 --logger.level debug > tmp\streamlit_debug.log 2>&1
echo Streamlit exited. See tmp\streamlit_debug.log
pause
