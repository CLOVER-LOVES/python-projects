# Hey Clover Voice Assistant

A powerful, modular voice assistant built in Python that can perform various tasks through voice commands, with advanced features like "Hey Clover" wake word detection, GPT integration, smart home control, system control, and a graphical user interface. It runs in the background with minimal resource usage, similar to how Siri works on Apple devices.

## Features

### Core Features
- **Voice Recognition**: Listens to your commands and responds with speech
- **Modular Command System**: Easily extendable with new commands
- **Wikipedia Search**: Search for information on Wikipedia
- **Web Browsing**: Open popular websites with voice commands
- **Email**: Send emails through voice commands
- **Weather Information**: Get current weather for any city
- **Reminders**: Set and manage reminders
- **Notes**: Take and read back notes
- **Music Playback**: Play music from your local library
- **Time Information**: Ask for the current time

### Advanced Features
- **Wake Word Detection**: Activate the assistant hands-free using wake words like "Jarvis" or "Computer"
- **GPT Integration**: Have more natural conversations using OpenAI's GPT models
- **Smart Home Control**: Control your smart home devices with voice commands
- **Graphical User Interface**: Visual interface showing conversation history and status
- **System Control**: Control your laptop's functions like a true digital assistant
  - Volume and brightness control
  - Power management (shutdown, restart, sleep, lock)
  - Application management (launch and close apps)
  - System information (battery, CPU, memory, disk)
  - Screenshots and file operations

## Requirements

- Python 3.6+
- Required Python packages (install with `pip install -r requirements.txt`):
  - pyttsx3
  - SpeechRecognition
  - wikipedia
  - requests
  - pyaudio
  - python-dotenv
  - openai (for GPT integration)
  - pvporcupine (for wake word detection)
  - pillow (for GUI)

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the assistant:
   ```
   run_hey_clover.bat          # Main launcher with all options
   ```

   Or use specific batch files:
   ```
   start_assistant.bat         # Background mode (recommended)
   run_advanced_assistant.bat  # Advanced features with GUI
   run_assistant.bat           # Basic assistant
   ```

   You can also run the Python scripts directly:
   ```
   python background_assistant.py --start  # Background mode
   python advanced_assistant.py            # Advanced features with GUI
   python main.py                          # Basic assistant
   ```

## First-Time Setup

### Basic Setup
On first run, the assistant will guide you through a configuration process:

1. Voice selection (male/female)
2. Email setup (for sending emails)
3. Weather API setup (requires an OpenWeatherMap API key)
4. Music directory configuration

You can also trigger this setup later by saying "configure assistant" or "setup assistant".

### Advanced Setup
The advanced assistant has additional configuration options:

1. Wake Word Detection setup (requires a Picovoice access key)
2. GPT Integration setup (requires an OpenAI API key)
3. Smart Home Control setup
4. GUI preferences

### Background Mode Setup
To run the assistant in the background like Siri:

1. Make sure you've configured the wake word "Hey Clover" with a valid Picovoice access key
2. Run `start_assistant.bat` or select option 1 in the main launcher
3. The assistant will run in the background with minimal resource usage
4. Control it from the system tray icon in the notification area
5. To make it start automatically with Windows, select option 4 in the main launcher

## Configuration

### Basic Configuration
The assistant uses a `config.json` file to store basic settings. You can edit this file directly if needed:

```json
{
    "email": {
        "sender": "your-email@gmail.com",
        "password": "your-app-password",
        "recipients": {
            "john": "john@example.com"
        }
    },
    "paths": {
        "music_dir": "D:\\Music",
        "code_editor": "C:\\Path\\To\\Editor.exe"
    },
    "weather_api_key": "your-api-key",
    "voice": 0,
    "wake_word": "assistant"
}
```

### Advanced Configuration
The advanced features use an `advanced_config.json` file:

```json
{
    "wake_word": {
        "enabled": true,
        "keywords": ["jarvis", "computer"],
        "sensitivity": 0.5,
        "access_key": "your-picovoice-access-key"
    },
    "gpt": {
        "enabled": true,
        "api_key": "your-openai-api-key",
        "model": "gpt-3.5-turbo",
        "use_for_unknown_commands": true
    },
    "smart_home": {
        "enabled": true,
        "config_file": "smart_home_config.json"
    },
    "gui": {
        "enabled": true,
        "theme": "light"
    }
}
```

### Smart Home Configuration
Smart home devices are configured in `smart_home_config.json`:

```json
{
    "platforms": {
        "hue": {
            "enabled": true,
            "bridge_ip": "192.168.1.100",
            "username": "your-hue-username"
        },
        "home_assistant": {
            "enabled": true,
            "url": "http://homeassistant.local:8123",
            "token": "your-long-lived-access-token"
        }
    },
    "device_aliases": {
        "living room light": "hue:1",
        "kitchen light": "hue:2",
        "tv": "home_assistant:media_player.tv"
    }
}
```

## Available Commands

### Basic Commands
Here are some examples of basic commands you can use:

- **Wikipedia**: "Search Wikipedia for Python programming"
- **Web Browsing**: "Open YouTube", "Open Google", "Open Stack Overflow"
- **Time**: "What's the time?", "Tell me the time"
- **Email**: "Send an email to John"
- **Weather**: "What's the weather in London?", "How's the weather in New York?"
- **Reminders**: "Remind me to call mom", "Set a reminder for meeting"
- **Notes**: "Take a note", "Make a note", "Read my notes"
- **Music**: "Play music"
- **Exit**: "Exit", "Quit", "Goodbye"

### Advanced Commands
With the advanced features enabled, you can also use:

- **Wake Word**: Say "Hey Clover" to activate the assistant hands-free
- **GPT Chat**: "Hey Clover, chat with GPT about Python programming", or any question for a natural conversation
- **Smart Home**: "Hey Clover, turn on living room light", "Hey Clover, turn off kitchen light", "Hey Clover, set temperature to 72 degrees"
- **GUI Controls**: Use the graphical interface to start/stop listening, configure settings, and view conversation history
- **System Control**:
  - **Volume**: "Hey Clover, turn up the volume", "Hey Clover, lower the volume", "Hey Clover, set volume to 50 percent", "Hey Clover, mute"
  - **Brightness**: "Hey Clover, set brightness to 75 percent"
  - **Power**: "Hey Clover, shutdown computer", "Hey Clover, restart computer", "Hey Clover, put computer to sleep", "Hey Clover, lock computer"
  - **Applications**: "Hey Clover, open Notepad", "Hey Clover, launch Chrome", "Hey Clover, close Calculator"
  - **Screenshots**: "Hey Clover, take a screenshot"
  - **System Info**: "Hey Clover, what's my battery status", "Hey Clover, how much memory am I using", "Hey Clover, check CPU usage"
  - **Files**: "Hey Clover, find files named report", "Hey Clover, create folder Projects"

## Adding New Commands

The assistant uses a modular command system. To add a new command:

1. Create a new class that inherits from the `Command` base class
2. Implement the `matches()` and `execute()` methods
3. Add an instance of your command to the `initialize_commands()` method in the `VoiceAssistant` class

Example:

```python
class MyNewCommand(Command):
    def matches(self, query: str) -> bool:
        return 'my command phrase' in query

    def execute(self, query: str) -> bool:
        # Your command logic here
        self.assistant.speak("Command executed!")
        return True
```

## Testing

Run the unit tests to verify the assistant's functionality:

```
python test_voice_assistant.py
```

## Troubleshooting

### Basic Features
- **Microphone not working**: Make sure your microphone is properly connected and set as the default recording device
- **Speech recognition errors**: Speak clearly and reduce background noise
- **Email sending fails**: Make sure you're using an app password if you have 2FA enabled
- **Weather information not available**: Verify your API key is correct

### Advanced Features
- **Wake word detection not working**: Ensure you have a valid Picovoice access key and that pvporcupine is installed
- **GPT integration not responding**: Check your OpenAI API key and internet connection
- **Smart home control failing**: Verify your smart home platform credentials and network connectivity
- **GUI not displaying properly**: Make sure you have pillow installed and try adjusting your screen resolution
- **System control issues**:
  - **Volume/brightness control not working**: Make sure you have the required permissions to control system settings
  - **Application control failing**: Verify the application names and paths
  - **System information errors**: Ensure psutil is properly installed
  - **Screenshot errors**: Check that pyautogui is installed correctly

### Background Mode Issues
- **System tray icon not appearing**: Make sure pystray is installed correctly
- **High resource usage**: Check the background_assistant.log file for errors
- **Assistant not starting automatically**: Verify that the startup shortcut was created correctly
- **Wake word not detected**: Speak clearly and directly toward your microphone
- **Assistant not responding**: Try restarting the background service

## License

This project is licensed under the MIT License - see the LICENSE file for details.
