---
layout: default
title: French Learning Bot
---

# French Learning Bot

A Telegram bot that helps users learn French by sending daily vocabulary, weekly quizzes, and progress reports.

![French Bot Demo](assets/images/french-bot-demo.png)

## Features

- **Daily Vocabulary**: Receive 10 new French words or phrases every day
- **Weekly Quizzes**: Test your knowledge with quizzes sent every Sunday
- **Progress Tracking**: Monitor your learning progress with weekly reports
- **Customized Content**: Different types of content based on the day of the week:
  - Monday: Common French phrases
  - Tuesday: French verbs with conjugations
  - Wednesday: French adjectives
  - Thursday: French idioms
  - Friday: Food-related vocabulary
  - Saturday: Business/professional terms
  - Sunday: Slang expressions

## Components

- `telegrambot.py` - Main script for the French learning bot
- `chat2.py` - Simplified version that sends daily French verbs
- `HUG.py` - Script to display random French verbs from a CSV file
- `verbs.csv` - Database of French verbs with meanings and examples

## Usage

```bash
# Run the main Telegram bot that sends daily vocabulary, quizzes, and progress reports
chatbot/run_french_bot.bat

# Run the simplified version that only sends daily French verbs
chatbot/run_chat2.bat

# Display random French verbs from the CSV file
chatbot/run_hug.bat
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/CLOVER-LOVES/python-projects.git
   cd python-projects
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the chatbot directory with your API keys:
   ```
   OPENAI_API_KEY="your-openai-api-key"
   TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
   TELEGRAM_CHAT_ID="your-telegram-chat-id"
   ```

4. Run the bot:
   ```bash
   chatbot/run_french_bot.bat
   ```

## How to Get Telegram Bot Token and Chat ID

1. **Create a Telegram Bot**:
   - Open Telegram and search for "BotFather"
   - Send the command `/newbot`
   - Follow the instructions to create a new bot
   - BotFather will give you a token for your bot

2. **Get Your Chat ID**:
   - Start a chat with your bot
   - Send a message to your bot
   - Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Look for the "chat" object and find the "id" field

[Back to Home](index.html)
