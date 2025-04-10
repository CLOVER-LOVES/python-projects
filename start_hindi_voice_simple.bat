@echo off
color 0A
cls
echo =====================================================
echo       VOICE ASSISTANT WITH HINDI VOICE
echo =====================================================
echo.
echo Starting voice assistant with Hindi voice...
echo.
echo Say "JARVIS" to activate the assistant
echo The assistant will respond in Hindi
echo.
echo =====================================================
echo.

REM Create a temporary Python script to set up Hindi voice
echo import json > temp_hindi_setup.py
echo config_file = "voice_enhancements.json" >> temp_hindi_setup.py
echo try: >> temp_hindi_setup.py
echo     with open(config_file, 'r') as f: >> temp_hindi_setup.py
echo         config = json.load(f) >> temp_hindi_setup.py
echo     config["tts"]["engine"] = "gtts" >> temp_hindi_setup.py
echo     config["tts"]["language"] = "hi" >> temp_hindi_setup.py
echo     with open(config_file, 'w') as f: >> temp_hindi_setup.py
echo         json.dump(config, f, indent=4) >> temp_hindi_setup.py
echo     print("Hindi voice configured successfully!") >> temp_hindi_setup.py
echo except Exception as e: >> temp_hindi_setup.py
echo     print(f"Error configuring Hindi voice: {e}") >> temp_hindi_setup.py

REM Run the setup script
python temp_hindi_setup.py

REM Delete the temporary script
del temp_hindi_setup.py

REM Start the background assistant
python background_assistant.py --start

echo.
echo If the assistant doesn't start, check the log files for errors.
pause
