# Python Projects Collection

This repository contains a collection of Python projects, including voice assistants and language learning bots.

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

### Running the Projects

#### Voice Assistant
- Run `python voice_assistant/enhanced_voice_assistant.py` for the basic assistant
- Run `python voice_assistant/advanced_assistant.py` for the advanced assistant
- Run `start_hindi_voice_simple.bat` to use the Hindi voice

#### French Learning Bot
- Run `chatbot/run_french_bot.bat` for the main Telegram bot
- Run `chatbot/run_chat2.bat` for the simplified version
- Run `chatbot/run_hug.bat` to display random French verbs

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
