import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import json
import requests
import logging
import time
import threading
from typing import Optional, Dict, List, Any, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("assistant.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Command:
    """Base class for all commands"""
    def __init__(self, assistant):
        self.assistant = assistant
    
    def matches(self, query: str) -> bool:
        """Check if this command matches the query"""
        raise NotImplementedError("Subclasses must implement matches()")
    
    def execute(self, query: str) -> bool:
        """Execute the command. Return True if handled, False otherwise."""
        raise NotImplementedError("Subclasses must implement execute()")

class WikipediaCommand(Command):
    """Search Wikipedia"""
    def matches(self, query: str) -> bool:
        return 'wikipedia' in query
    
    def execute(self, query: str) -> bool:
        self.assistant.speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            self.assistant.speak("According to Wikipedia")
            print(results)
            self.assistant.speak(results)
            return True
        except Exception as e:
            logger.error(f"Error searching Wikipedia: {e}")
            self.assistant.speak("Sorry, I couldn't find that information on Wikipedia.")
            return False

class WebBrowserCommand(Command):
    """Open websites"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.sites = {
            'youtube': 'youtube.com',
            'google': 'google.com',
            'stackoverflow': 'stackoverflow.com',
            'github': 'github.com',
            'mail': 'mail.google.com'
        }
    
    def matches(self, query: str) -> bool:
        return any(f'open {site}' in query for site in self.sites.keys())
    
    def execute(self, query: str) -> bool:
        for site, url in self.sites.items():
            if f'open {site}' in query:
                try:
                    webbrowser.open(url)
                    self.assistant.speak(f"Opening {site}")
                    return True
                except Exception as e:
                    logger.error(f"Error opening {site}: {e}")
                    self.assistant.speak(f"Sorry, I couldn't open {site}")
                    return False
        return False

class MusicCommand(Command):
    """Play music"""
    def matches(self, query: str) -> bool:
        return 'play music' in query
    
    def execute(self, query: str) -> bool:
        music_dir = self.assistant.config['paths'].get('music_dir', '')
        if not music_dir or not os.path.exists(music_dir):
            self.assistant.speak("Music directory not found or not configured")
            return False
        
        try:
            songs = os.listdir(music_dir)
            if not songs:
                self.assistant.speak("No music files found in the specified directory")
                return False
            
            os.startfile(os.path.join(music_dir, songs[0]))
            self.assistant.speak("Playing music")
            return True
        except Exception as e:
            logger.error(f"Error playing music: {e}")
            self.assistant.speak("Sorry, I couldn't play music")
            return False

class TimeCommand(Command):
    """Tell the time"""
    def matches(self, query: str) -> bool:
        return 'the time' in query
    
    def execute(self, query: str) -> bool:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.assistant.speak(f"The time is {str_time}")
        return True

class EmailCommand(Command):
    """Send email"""
    def matches(self, query: str) -> bool:
        return 'email' in query or 'send mail' in query
    
    def execute(self, query: str) -> bool:
        # Check if email is configured
        email_config = self.assistant.config.get('email', {})
        if not email_config.get('sender') or not email_config.get('password'):
            self.assistant.speak("Email is not configured. Please update your configuration.")
            return False
        
        # Ask for recipient
        self.assistant.speak("Who would you like to send an email to?")
        recipient_name = self.assistant.take_command()
        if not recipient_name:
            return False
        
        # Check if recipient exists in contacts
        recipients = email_config.get('recipients', {})
        recipient_email = recipients.get(recipient_name.lower())
        
        if not recipient_email:
            self.assistant.speak(f"I don't have an email address for {recipient_name}. Would you like to add one?")
            response = self.assistant.take_command()
            if response and ('yes' in response.lower() or 'sure' in response.lower()):
                self.assistant.speak("Please say the email address")
                email_address = self.assistant.take_command()
                if email_address:
                    # Clean up the email address (remove spaces, etc.)
                    email_address = ''.join(email_address.split()).lower()
                    if '@' in email_address and '.' in email_address:
                        if 'recipients' not in email_config:
                            email_config['recipients'] = {}
                        email_config['recipients'][recipient_name.lower()] = email_address
                        self.assistant.config['email'] = email_config
                        self.assistant.save_config()
                        recipient_email = email_address
                        self.assistant.speak(f"Added {recipient_name} with email {email_address}")
                    else:
                        self.assistant.speak("That doesn't appear to be a valid email address")
                        return False
            else:
                return False
        
        # Ask for content
        self.assistant.speak("What should I say?")
        content = self.assistant.take_command()
        if not content:
            return False
        
        # Send email
        try:
            if self.assistant.send_email(recipient_email, content):
                self.assistant.speak("Email has been sent!")
                return True
            else:
                self.assistant.speak("Sorry, I couldn't send the email")
                return False
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            self.assistant.speak("Sorry, I encountered an error while sending the email")
            return False

class WeatherCommand(Command):
    """Get weather information"""
    def matches(self, query: str) -> bool:
        return 'weather' in query
    
    def execute(self, query: str) -> bool:
        # Check if a city is mentioned in the query
        city = None
        query_words = query.split()
        for i, word in enumerate(query_words):
            if word == 'in' and i < len(query_words) - 1:
                city = query_words[i + 1]
                break
        
        if not city:
            self.assistant.speak("Which city would you like to know the weather for?")
            city_response = self.assistant.take_command()
            if city_response:
                city = city_response.split()[0]  # Take the first word as the city
            else:
                return False
        
        weather_info = self.assistant.get_weather(city)
        if weather_info:
            self.assistant.speak(weather_info)
            return True
        else:
            self.assistant.speak(f"Sorry, I couldn't get the weather information for {city}")
            return False

class ReminderCommand(Command):
    """Set reminders"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.reminders = []
        self.reminder_thread = None
        self.stop_flag = threading.Event()
        self.start_reminder_checker()
    
    def matches(self, query: str) -> bool:
        return 'remind' in query or 'reminder' in query
    
    def execute(self, query: str) -> bool:
        if 'list' in query or 'show' in query:
            return self.list_reminders()
        else:
            return self.set_reminder()
    
    def set_reminder(self) -> bool:
        self.assistant.speak("What would you like me to remind you about?")
        reminder_text = self.assistant.take_command()
        if not reminder_text:
            return False
        
        self.assistant.speak("When should I remind you? Please specify the time.")
        time_text = self.assistant.take_command()
        if not time_text:
            return False
        
        try:
            # Very basic time parsing - could be improved
            hour = None
            minute = 0
            
            if ":" in time_text:
                time_parts = time_text.split(":")
                hour = int(time_parts[0])
                minute = int(time_parts[1].split()[0])
            else:
                for word in time_text.split():
                    if word.isdigit():
                        hour = int(word)
            
            if hour is None:
                self.assistant.speak("I couldn't understand the time. Please try again.")
                return False
            
            # Check for AM/PM
            if 'p.m.' in time_text.lower() or 'pm' in time_text.lower():
                if hour < 12:
                    hour += 12
            elif 'a.m.' in time_text.lower() or 'am' in time_text.lower():
                if hour == 12:
                    hour = 0
            
            # Create reminder time
            now = datetime.datetime.now()
            reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If the time is in the past, assume it's for tomorrow
            if reminder_time < now:
                reminder_time += datetime.timedelta(days=1)
            
            self.reminders.append({
                'text': reminder_text,
                'time': reminder_time,
                'notified': False
            })
            
            time_str = reminder_time.strftime("%I:%M %p")
            self.assistant.speak(f"Okay, I'll remind you to {reminder_text} at {time_str}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting reminder: {e}")
            self.assistant.speak("Sorry, I couldn't set that reminder")
            return False
    
    def list_reminders(self) -> bool:
        if not self.reminders:
            self.assistant.speak("You don't have any reminders set.")
            return True
        
        self.assistant.speak("Here are your reminders:")
        for i, reminder in enumerate(self.reminders):
            if not reminder['notified']:
                time_str = reminder['time'].strftime("%I:%M %p")
                self.assistant.speak(f"{i+1}. {reminder['text']} at {time_str}")
        
        return True
    
    def start_reminder_checker(self):
        """Start the reminder checker thread"""
        if self.reminder_thread is None or not self.reminder_thread.is_alive():
            self.stop_flag.clear()
            self.reminder_thread = threading.Thread(target=self.check_reminders)
            self.reminder_thread.daemon = True
            self.reminder_thread.start()
    
    def check_reminders(self):
        """Check for due reminders periodically"""
        while not self.stop_flag.is_set():
            now = datetime.datetime.now()
            for reminder in self.reminders:
                if not reminder['notified'] and now >= reminder['time']:
                    self.assistant.speak(f"Reminder: {reminder['text']}")
                    reminder['notified'] = True
            time.sleep(30)  # Check every 30 seconds

class NoteCommand(Command):
    """Take notes"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.notes_file = "assistant_notes.txt"
    
    def matches(self, query: str) -> bool:
        return ('take a note' in query or 'make a note' in query or 
                'write this down' in query or 'remember this' in query)
    
    def execute(self, query: str) -> bool:
        self.assistant.speak("What would you like me to note down?")
        note_text = self.assistant.take_command()
        if not note_text:
            return False
        
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.notes_file, "a") as f:
                f.write(f"[{timestamp}] {note_text}\n")
            
            self.assistant.speak("I've made a note of that")
            return True
        except Exception as e:
            logger.error(f"Error taking note: {e}")
            self.assistant.speak("Sorry, I couldn't save that note")
            return False

class ReadNotesCommand(Command):
    """Read saved notes"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.notes_file = "assistant_notes.txt"
    
    def matches(self, query: str) -> bool:
        return 'read' in query and 'note' in query
    
    def execute(self, query: str) -> bool:
        try:
            if not os.path.exists(self.notes_file):
                self.assistant.speak("You don't have any saved notes yet.")
                return True
            
            with open(self.notes_file, "r") as f:
                notes = f.readlines()
            
            if not notes:
                self.assistant.speak("You don't have any saved notes yet.")
                return True
            
            self.assistant.speak("Here are your notes:")
            for note in notes[-5:]:  # Read the 5 most recent notes
                self.assistant.speak(note.strip())
            
            return True
        except Exception as e:
            logger.error(f"Error reading notes: {e}")
            self.assistant.speak("Sorry, I couldn't read your notes")
            return False

class VoiceAssistant:
    def __init__(self):
        try:
            self.engine = pyttsx3.init('sapi5')
            self.voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', self.voices[0].id)
            self.load_config()
            self.initialize_commands()
            logger.info("Voice Assistant initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Voice Assistant: {e}")
            print(f"Error initializing Voice Assistant: {e}")
            raise

    def load_config(self):
        """Load configuration from config file"""
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
            logger.info("Configuration loaded successfully")
        except FileNotFoundError:
            logger.warning("Config file not found, creating default configuration")
            self.config = {
                'email': {
                    'sender': '',
                    'password': '',
                    'recipients': {}
                },
                'paths': {
                    'music_dir': '',
                    'code_editor': ''
                },
                'weather_api_key': '',
                'voice': 0,  # 0 for male, 1 for female
                'wake_word': 'assistant'
            }
            self.save_config()

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")

    def initialize_commands(self):
        """Initialize all available commands"""
        self.commands = [
            WikipediaCommand(self),
            WebBrowserCommand(self),
            MusicCommand(self),
            TimeCommand(self),
            EmailCommand(self),
            WeatherCommand(self),
            ReminderCommand(self),
            NoteCommand(self),
            ReadNotesCommand(self)
        ]
        logger.info(f"Initialized {len(self.commands)} commands")

    def speak(self, text: str) -> None:
        """Convert text to speech"""
        try:
            print(f"Assistant: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in speech synthesis: {e}")
            print(f"Error in speech synthesis: {e}")

    def wish_me(self) -> None:
        """Greet user based on time of day"""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("I am your voice assistant. How may I help you?")

    def take_command(self) -> Optional[str]:
        """Take microphone input and return string output"""
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"User said: {query}\n")
                return query.lower()
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            print(f"Error in speech recognition: {e}")
            return None

    def send_email(self, to: str, content: str) -> bool:
        """Send email using configured settings"""
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(self.config['email']['sender'], self.config['email']['password'])
            server.sendmail(self.config['email']['sender'], to, content)
            server.close()
            logger.info(f"Email sent successfully to {to}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    def get_weather(self, city: str) -> Optional[str]:
        """Get weather information for a city"""
        try:
            api_key = self.config.get('weather_api_key', '')
            if not api_key:
                self.speak("Weather API key is not configured")
                return None
                
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                humidity = data['main']['humidity']
                return f"The temperature in {city} is {temp}°C with {desc}. The humidity is {humidity}%."
            else:
                logger.error(f"Weather API error: {data.get('message', 'Unknown error')}")
                return None
        except Exception as e:
            logger.error(f"Error getting weather: {e}")
            return None

    def process_command(self, query: str) -> None:
        """Process user commands"""
        try:
            # Check if any command matches and can handle the query
            for command in self.commands:
                if command.matches(query):
                    if command.execute(query):
                        return
            
            # If no command matched
            self.speak("I'm not sure how to help with that")
            
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self.speak("Sorry, I encountered an error while processing your request")

    def configure_assistant(self):
        """Interactive configuration of the assistant"""
        self.speak("Let's configure your assistant")
        
        # Configure voice
        self.speak("Would you prefer a male or female voice?")
        voice_choice = self.take_command()
        if voice_choice and ('female' in voice_choice or 'woman' in voice_choice):
            if len(self.voices) > 1:
                self.engine.setProperty('voice', self.voices[1].id)
                self.config['voice'] = 1
                self.speak("Female voice selected")
            else:
                self.speak("Sorry, female voice is not available on your system")
        else:
            self.engine.setProperty('voice', self.voices[0].id)
            self.config['voice'] = 0
            self.speak("Male voice selected")
        
        # Configure email
        self.speak("Would you like to set up email functionality?")
        email_choice = self.take_command()
        if email_choice and ('yes' in email_choice or 'sure' in email_choice):
            self.speak("Please enter your email address in the console")
            email = input("Email address: ")
            self.speak("Please enter your app password in the console")
            password = input("App password: ")
            self.config['email']['sender'] = email
            self.config['email']['password'] = password
            self.speak("Email configuration saved")
        
        # Configure weather
        self.speak("Would you like to set up weather functionality?")
        weather_choice = self.take_command()
        if weather_choice and ('yes' in weather_choice or 'sure' in weather_choice):
            self.speak("Please enter your OpenWeatherMap API key in the console")
            api_key = input("API key: ")
            self.config['weather_api_key'] = api_key
            self.speak("Weather configuration saved")
        
        # Configure music directory
        self.speak("Would you like to set up your music directory?")
        music_choice = self.take_command()
        if music_choice and ('yes' in music_choice or 'sure' in music_choice):
            self.speak("Please enter your music directory path in the console")
            music_dir = input("Music directory path: ")
            self.config['paths']['music_dir'] = music_dir
            self.speak("Music directory saved")
        
        self.save_config()
        self.speak("Configuration complete")

    def run(self):
        """Main loop for the voice assistant"""
        self.wish_me()
        
        # Check if this is the first run or if configuration is incomplete
        if not self.config['email']['sender'] or not self.config['weather_api_key']:
            self.speak("It looks like your assistant is not fully configured. Would you like to set it up now?")
            setup_response = self.take_command()
            if setup_response and ('yes' in setup_response or 'sure' in setup_response):
                self.configure_assistant()
        
        while True:
            query = self.take_command()
            if query:
                if 'exit' in query or 'quit' in query or 'goodbye' in query:
                    self.speak("Goodbye! Have a great day!")
                    break
                elif 'configure' in query or 'setup' in query:
                    self.configure_assistant()
                else:
                    self.process_command(query)

if __name__ == "__main__":
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        print(f"Critical error: {e}")
