@echo off
echo ===================================
echo Hey Clover Voice Assistant Launcher
echo ===================================
echo.
echo Choose an option:
echo 1. Start Hey Clover in background (recommended)
echo 2. Start advanced assistant with GUI
echo 3. Start basic assistant
echo 4. Install as startup program
echo 5. Exit
echo.

choice /C 12345 /N /M "Enter your choice (1-5): "

if errorlevel 5 goto exit
if errorlevel 4 goto install
if errorlevel 3 goto basic
if errorlevel 2 goto advanced
if errorlevel 1 goto background

:background
echo.
echo Starting Hey Clover in background mode...
start /min python background_assistant.py --start
echo Hey Clover is now running in the background.
echo Look for the icon in your system tray.
goto end

:advanced
echo.
echo Starting advanced assistant with GUI...
python advanced_assistant.py
goto end

:basic
echo.
echo Starting basic assistant...
python main.py
goto end

:install
echo.
echo Installing Hey Clover as a startup program...
python install_service.py --startup
echo.
echo Hey Clover will now start automatically when you log in to Windows.
goto end

:exit
echo.
echo Exiting...
goto end

:end
echo.
echo Thank you for using Hey Clover Voice Assistant!
timeout /t 5
