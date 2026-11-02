@echo off
title AarogyaSarvam - Sarvam AI Healthcare Agent
echo ===================================================================
echo 🏥 AarogyaSarvam - Multilingual Healthcare & Cashless Insurance AI
echo ===================================================================
echo Starting server...
echo Access the website at: http://127.0.0.1:8000 or http://localhost:8000
echo ===================================================================
echo.
"C:\Program Files\Python313\python.exe" app.py
if %ERRORLEVEL% NEQ 0 (
    python app.py
)
pause
