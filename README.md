# Python Projects Collection

- IN DEVELOPING
  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://github.com/CLOVER-LOVES/python-projects/actions/workflows/python-app.yml/badge.svg)](https://github.com/CLOVER-LOVES/python-projects/actions)

This repository contains a collection of Python projects, including voice assistants and language learning bots. These projects demonstrate various Python programming concepts and practical applications.

## Table of Contents

- [Projects](#projects)
  - [Voice Assistant](#voice-assistant)
  - [French Learning Bot](#french-learning-bot)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)

## Projects

### Voice Assistant

A voice-controlled assistant that can perform various tasks on your laptop, similar to Siri on iPhone. The assistant can be configured to speak in different languages, including Hindi.

#### Features:
- Voice recognition and text-to-speech capabilities
- Wake word detection ("Hey Clover", "Jarvis", etc.)
- Email sending functionality
- Weather information retrieval
- Music playback control
- Web browsing
- Smart home device control
- Note-taking and reminders
- GPT integration for natural language conversations

#### Configuration:
The voice assistant uses several configuration files:
- `config.json` - Basic configuration
- `advanced_config.json` - Advanced features configuration
- `smart_home_config.json` - Smart home devices configuration
- `voice_enhancements.json` - Voice enhancement configuration

### French Learning Bot

A Telegram bot that helps users learn French by sending daily vocabulary, weekly quizzes, and progress reports.

#### Features:
- Daily French vocabulary with meanings and examples
- Weekly quizzes to test knowledge
- Progress tracking and reporting
- Customizable content based on the day of the week

#### Components:
- `telegrambot.py` - Main script for the French learning bot
- `chat2.py` - Simplified version that sends daily French verbs
- `HUG.py` - Script to display random French verbs from a CSV file
- `verbs.csv` - Database of French verbs with meanings and examples

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - openai
  - python-dotenv
  - requests
  - schedule
  - pyttsx3 (for voice assistant)
  - SpeechRecognition (for voice assistant)
  - gTTS (for Hindi voice)

### Environment Variables
Create a `.env` file in the chatbot directory with the following variables:
```
OPENAI_API_KEY="your-openai-api-key"
TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
TELEGRAM_CHAT_ID="your-telegram-chat-id"
```

## Usage

### Voice Assistant

```bash
# Run the basic voice assistant
python voice_assistant/enhanced_voice_assistant.py

# Run the advanced voice assistant with more features
python voice_assistant/advanced_assistant.py

# Run the voice assistant with Hindi voice
start_hindi_voice_simple.bat
```

The voice assistant responds to commands like:
- "What time is it?"
- "Open Google"
- "Play music"
- "Send an email to [recipient]"
- "What's the weather like?"
- "Set a reminder for [time]"

### French Learning Bot

```bash
# Run the main Telegram bot that sends daily vocabulary, quizzes, and progress reports
chatbot/run_french_bot.bat

# Run the simplified version that only sends daily French verbs
chatbot/run_chat2.bat

# Display random French verbs from the CSV file
chatbot/run_hug.bat
```

The French Learning Bot will:
- Send daily French vocabulary to your Telegram account
- Send weekly quizzes on Sundays
- Send progress reports on Saturdays
- Track your learning progress

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
