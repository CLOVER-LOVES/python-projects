@echo off
color 0A
cls
echo =====================================================
echo       VOICE ASSISTANT WITH JARVIS WAKE WORD
echo =====================================================
echo.
echo IMPORTANT INSTRUCTIONS:
echo ---------------------
echo 1. The assistant is configured to use "JARVIS" as the wake word
echo    (This avoids conflicts with "Hey Google")
echo.
echo 2. To activate the assistant, say "JARVIS" clearly
echo    Example: "JARVIS, what time is it?"
echo.
echo 3. The assistant will still respond as "Hey Clover"
echo.
echo 4. If you want to use a different wake word, edit the
echo    voice_enhancements.json file
echo.
echo =====================================================
echo.
echo Starting voice assistant in background mode...
echo.
python background_assistant.py --start
echo.
echo If the assistant doesn't start, check the log files for errors.
pause
