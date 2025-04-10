# Hey Clover Voice Assistant

A comprehensive voice assistant for Windows that works like Siri for your laptop. This assistant can control your computer, answer questions, manage smart home devices, and more - all through voice commands.

## Quick Start

1. Run the main launcher:
   ```
   run_hey_clover.bat
   ```

2. Choose option 1 to start the assistant in background mode

3. Say "Hey Clover" followed by your command

## Features

- **Always Listening**: Runs in the background with minimal resource usage
- **Natural Voice**: Uses advanced TTS engines for more human-like responses
- **System Control**: Control volume, brightness, power, applications, and more
- **Smart Home Integration**: Control compatible smart home devices
- **AI Conversations**: Chat naturally using OpenAI's GPT models
- **File Management**: Search for files, create folders, and more
- **Information Retrieval**: Get weather, time, and web information
- **Reminders & Notes**: Set reminders and take notes

## File Organization

### Core Files
- `run_hey_clover.bat` - Main launcher script
- `README.md` - Detailed documentation
- `requirements.txt` - Required dependencies

### Assistant Implementations
- `background_assistant.py` - Background service implementation (recommended)
- `advanced_assistant.py` - Advanced assistant with all features
- `enhanced_voice_assistant.py` - Enhanced assistant implementation
- `main.py` - Basic assistant entry point

### Voice Enhancement Files
- `custom_wake_word.py` - "Hey Clover" wake word implementation
- `advanced_tts.py` - Advanced text-to-speech engines
- `voice_enhancements.py` - Integration of wake word and TTS

### Feature Modules
- `system_control.py` - System control functionality
- `system_commands.py` - System control commands
- `gpt_integration.py` - OpenAI GPT integration
- `smart_home.py` - Smart home control
- `gui_assistant.py` - Graphical user interface

### Utility Files
- `install_service.py` - Service installation script
- `start_assistant.bat` - Background mode starter
- `run_advanced_assistant.bat` - Advanced mode starter
- `run_assistant.bat` - Basic mode starter

### Documentation
- `README.md` - Main documentation
- `background_service_README.md` - Background service documentation

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the assistant:
   ```
   run_hey_clover.bat
   ```

## Configuration

The assistant uses several configuration files:
- `config.json` - Basic configuration
- `advanced_config.json` - Advanced features configuration
- `smart_home_config.json` - Smart home devices configuration
- `voice_enhancements.json` - Voice enhancement configuration (created on first run)

## Required API Keys

For full functionality, you'll need:
1. **Picovoice Access Key** - For "Hey Clover" wake word detection (required)
2. **OpenAI API Key** - For GPT integration (optional)
3. **ElevenLabs API Key** - For premium voice quality (optional)
4. **OpenWeatherMap API Key** - For weather information (optional)

## Troubleshooting

If you encounter issues:
1. Check the log files (`assistant.log`, `background_assistant.log`)
2. Verify that all required dependencies are installed
3. Make sure you have valid API keys configured
4. Try restarting the assistant

## License

This project is licensed under the MIT License.
