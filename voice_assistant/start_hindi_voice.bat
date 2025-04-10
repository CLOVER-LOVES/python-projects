@echo off
color 0A
cls
echo =====================================================
echo       VOICE ASSISTANT WITH HINDI VOICE
echo =====================================================
echo.
echo IMPORTANT INSTRUCTIONS:
echo ---------------------
echo 1. The assistant is configured to use Hindi voice
echo    (Using Google Text-to-Speech with Hindi language)
echo.
echo 2. To activate the assistant, say "JARVIS" clearly
echo    Example: "JARVIS, namaste"
echo.
echo 3. The assistant will respond in Hindi
echo.
echo =====================================================
echo.
echo Starting voice assistant with Hindi voice...
echo.

python voice_assistant_hindi.py
echo.
echo If the assistant doesn't start, check the log files for errors.
pause
