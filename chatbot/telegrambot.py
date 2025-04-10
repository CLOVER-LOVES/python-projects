import openai
import requests
import json
import datetime
import os
from pathlib import Path
from dotenv import load_dotenv
import schedule
import time

# Load environment variables
load_dotenv()

# Get environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_daily_content():
    """Rotate between different types of French learning content"""
    day = datetime.datetime.now().weekday()

    prompts = {
        0: "Give me 10 common French phrases used in daily conversation with meanings and examples.",
        1: "Provide 10 French verbs with conjugations in present tense and example sentences.",
        2: "Share 10 French adjectives with their feminine/masculine forms and example usage.",
        3: "List 10 French idioms with their literal translations and actual meanings.",
        4: "Give me 10 French food-related vocabulary words with example dialogues.",
        5: "Provide 10 French business/professional terms with examples.",
        6: "Share 10 French slang expressions with their meanings and when to use them."
    }

    return prompts[day]

def get_french_vocab():
    """Get French vocabulary from OpenAI API"""
    try:
        prompt = get_daily_content()  # Get the day-specific prompt
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using 3.5-turbo for cost efficiency
            messages=[
                {"role": "system", "content": "You are a French language tutor."},
                {"role": "user", "content": prompt}
            ]
        )

        vocab = response.choices[0].message.content
        return vocab
    except Exception as e:
        print(f"Error getting vocabulary: {str(e)}")
        return None

def send_telegram_message(text):
    """Send vocabulary via Telegram bot"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🇫🇷 Your French Vocabulary for {datetime.date.today().strftime('%B %d, %Y')} 🇫🇷\n\n{text}",
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Vocabulary sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return False

def daily_task():
    """Daily task to send vocabulary"""
    print(f"\nSending vocabulary for {datetime.date.today().strftime('%B %d, %Y')}...")
    vocab = get_french_vocab()
    if vocab:
        send_telegram_message(vocab)

def run_scheduler():
    """Run the scheduler"""
    # Send vocabulary immediately on start
    daily_task()

    # Schedule daily vocabulary
    schedule.every().day.at("09:00").do(daily_task)

    # Schedule weekly quiz
    schedule.every().sunday.at("10:00").do(lambda: send_telegram_message(generate_quiz()))

    # Schedule weekly progress report
    schedule.every().saturday.at("18:00").do(send_progress_report)

    print("\nScheduler is running. Will send:")
    print("- Daily vocabulary at 09:00")
    print("- Weekly quiz on Sundays at 10:00")
    print("- Progress report on Saturdays at 18:00")
    print("Press Ctrl+C to stop")

    while True:
        schedule.run_pending()
        time.sleep(60)

def save_progress(vocab):
    """Save vocabulary and track progress"""
    try:
        file_path = Path("french_progress.json")
        today = datetime.date.today().isoformat()

        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"words_learned": 0, "days_streak": 0, "history": {}}

        # Update progress
        data["words_learned"] += 10
        data["history"][today] = vocab

        # Update streak
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        if yesterday in data["history"]:
            data["days_streak"] += 1
        else:
            data["days_streak"] = 1

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return data
    except Exception as e:
        print(f"Error saving progress: {str(e)}")
        return None

def send_progress_report():
    """Send weekly progress report"""
    try:
        with open('french_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        report = f"""📊 *Weekly Progress Report*
Words Learned: {data['words_learned']}
Current Streak: {data['days_streak']} days
Keep up the great work! 🎯"""

        send_telegram_message(report)
    except Exception as e:
        print(f"Error sending progress report: {str(e)}")

def generate_quiz():
    """Generate a quiz from recent vocabulary"""
    try:
        with open('french_progress.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Get recent words from history
        recent_words = list(data["history"].values())[-7:]  # Last 7 days

        prompt = f"""Create a 5-question quiz using these French words and phrases from the past week: {recent_words}.
Format as:
Q1. [Question]
a) [option]
b) [option]
c) [option]
d) [option]
Correct: [letter]

Use a mix of translation, fill-in-blanks, and usage questions."""

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a French language tutor."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating quiz: {str(e)}")
        return None

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")