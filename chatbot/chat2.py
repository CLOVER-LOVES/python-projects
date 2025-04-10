import openai
import os
import requests
import schedule
import time
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize OpenAI client

def get_french_verbs():
    """Fetches 10 new French verbs from OpenAI API."""
    prompt = """Give me 10 new French verbs along with their meanings and example sentences in this format:

Verb: [infinitive]
Meaning: [English translation]
Example: [French sentence]
Translation: [English sentence]

Make sure the verbs are different each day.
"""

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using 3.5-turbo for cost efficiency
        messages=[{"role": "system", "content": "You are a helpful French language assistant."},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def send_telegram_message():
    """Fetches verbs and sends them to Telegram bot."""
    verbs_text = get_french_verbs()
    message = f"📚 **Your Daily 10 French Verbs**:\n\n{verbs_text}"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)

    print(f"✅ Sent message: {response.json()}")  # Debugging

# Schedule the script to run daily at 9:00 AM
schedule.every().day.at("09:00").do(send_telegram_message)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait 60 seconds before checking again
