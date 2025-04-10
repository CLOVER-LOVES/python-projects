@echo off
echo ===================================
echo Hey Clover Voice Assistant Starter
echo ===================================
echo.
echo Starting Hey Clover in background mode...
echo.
echo NOTE: The wake word is set to "jarvis" but the assistant will respond to "Hey Clover"
echo       Just say "Hey Clover" followed by your command!
echo.
python background_assistant.py --start
echo.
echo If the assistant doesn't start, check the log files for errors.
pause
