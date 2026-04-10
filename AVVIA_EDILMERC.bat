@echo off
title EDILMERC 2026 - Avvio
echo ========================================
echo    EDILMERC 2026 - Gestionale
echo ========================================
echo.
echo Avvio dell'applicazione in corso...
echo.

REM Vai alla cartella del progetto
cd /d "c:\Users\danie\OneDrive\Desktop\CascadeProjects\personal-website"

REM Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo Installa Python da https://python.org
    pause
    exit /b 1
)

REM Avvia Streamlit
echo Avvio di Streamlit...
streamlit run modified_edilmerc.py

REM Se Streamlit non è installato, prova a installarlo
if errorlevel 1 (
    echo.
    echo Streamlit non trovato. Tentativo installazione...
    pip install streamlit
    echo.
    echo Riavvio dell'applicazione...
    streamlit run modified_edilmerc.py
)

echo.
echo Se l'applicazione non si apre, controlla:
echo 1. Python installato correttamente
echo 2. Streamlit installato
echo 3. Nessun firewall che blocca la porta 8501
echo.
pause
