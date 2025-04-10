@echo off
echo ===================================
echo Voice Assistant with Jarvis Wake Word
echo ===================================
echo.
echo Starting voice assistant in background mode...
echo.
echo IMPORTANT: The wake word is set to "jarvis" to avoid conflicts
echo            Say "Jarvis" to activate the assistant
echo            The assistant will still respond as "Hey Clover"
echo.
python background_assistant.py --start
echo.
echo If the assistant doesn't start, check the log files for errors.
pause
