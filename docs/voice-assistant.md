---
layout: default
title: Voice Assistant
---

# Voice Assistant

A voice-controlled assistant that can perform various tasks on your laptop, similar to Siri on iPhone. The assistant can be configured to speak in different languages, including Hindi.

![Voice Assistant Demo](assets/images/voice-assistant-demo.png)

## Features

- **Voice Recognition**: Understands spoken commands using speech recognition
- **Text-to-Speech**: Responds with natural-sounding voice
- **Wake Word Detection**: Activates with phrases like "Hey Clover" or "Jarvis"
- **Email Integration**: Send emails using voice commands
- **Weather Information**: Get current weather and forecasts
- **Music Control**: Play, pause, and control music playback
- **Web Browsing**: Open websites and search the web
- **Smart Home Control**: Control compatible smart home devices
- **Note Taking**: Create and read notes
- **Reminders**: Set and manage reminders
- **GPT Integration**: Natural language conversations using OpenAI's GPT

## Configuration

The voice assistant uses several configuration files:
- `config.json` - Basic configuration
- `advanced_config.json` - Advanced features configuration
- `smart_home_config.json` - Smart home devices configuration
- `voice_enhancements.json` - Voice enhancement configuration

## Usage

```bash
# Run the basic voice assistant
python voice_assistant/enhanced_voice_assistant.py

# Run the advanced voice assistant with more features
python voice_assistant/advanced_assistant.py

# Run the voice assistant with Hindi voice
start_hindi_voice_simple.bat
```

## Example Commands

- "What time is it?"
- "Open Google"
- "Play music"
- "Send an email to John"
- "What's the weather like?"
- "Set a reminder for 3 PM"
- "Turn on the living room light"
- "Take a note"
- "Read my notes"
- "Chat with GPT"

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CLOVER-LOVES/python-projects.git
   cd python-projects
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the assistant:
   - Edit `voice_assistant/config.json` with your settings
   - For advanced features, edit `voice_assistant/advanced_config.json`

4. Run the assistant:
   ```bash
   python voice_assistant/enhanced_voice_assistant.py
   ```

[Back to Home](index.html)
