"""
Advanced Voice Assistant
----------------------
This module integrates all the advanced features:
- GUI Interface
- Wake Word Detection
- GPT Integration
- Smart Home Control
"""

import os
import sys
import threading
import time
import json
import logging
import tkinter as tk
from typing import Optional, Dict, Any

# Import the enhanced voice assistant as the base
import enhanced_voice_assistant as base_assistant

# Import advanced features
try:
    from custom_wake_word import CustomWakeWordDetector as WakeWordDetector, get_available_keywords
    WAKE_WORD_AVAILABLE = True
except ImportError:
    print("Wake word detection not available. Install pvporcupine package.")
    WAKE_WORD_AVAILABLE = False

try:
    from gpt_integration import GPTAssistant
    GPT_AVAILABLE = True
except ImportError:
    print("GPT integration not available. Install openai package.")
    GPT_AVAILABLE = False

try:
    from smart_home import SmartHomeController
    SMART_HOME_AVAILABLE = True
except ImportError:
    print("Smart home control not available.")
    SMART_HOME_AVAILABLE = False

try:
    from gui_assistant import AssistantGUI
    GUI_AVAILABLE = True
except ImportError:
    print("GUI not available. Install pillow package.")
    GUI_AVAILABLE = False

try:
    from system_control import SystemControl
    from system_commands import get_system_commands
    SYSTEM_CONTROL_AVAILABLE = True
except ImportError:
    print("System control not available. Install required packages.")
    SYSTEM_CONTROL_AVAILABLE = False

# Import voice enhancements
try:
    from voice_enhancements import VoiceEnhancements
    VOICE_ENHANCEMENTS_AVAILABLE = True
except ImportError:
    print("Voice enhancements not available. Install required packages.")
    VOICE_ENHANCEMENTS_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("advanced_assistant.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedVoiceAssistant(base_assistant.VoiceAssistant):
    """
    Advanced Voice Assistant with additional features
    """
    def __init__(self, config_file="config.json"):
        """Initialize the advanced voice assistant"""
        super().__init__()

        # Load advanced configuration
        self.advanced_config = self.load_advanced_config()

        # Initialize advanced features
        self.wake_word_detector = None
        self.gpt_assistant = None
        self.smart_home = None
        self.gui = None
        self.voice_enhancements = None

        # Initialize available features
        self.initialize_advanced_features()

        # Add advanced commands
        self.add_advanced_commands()

        logger.info("Advanced Voice Assistant initialized")

    def load_advanced_config(self) -> Dict:
        """Load advanced configuration"""
        try:
            if os.path.exists("advanced_config.json"):
                with open("advanced_config.json", "r") as f:
                    return json.load(f)
            else:
                # Create default advanced configuration
                default_config = {
                    "wake_word": {
                        "enabled": WAKE_WORD_AVAILABLE,
                        "keywords": ["jarvis", "computer"],
                        "sensitivity": 0.5,
                        "access_key": ""
                    },
                    "gpt": {
                        "enabled": GPT_AVAILABLE,
                        "api_key": "",
                        "model": "gpt-3.5-turbo",
                        "use_for_unknown_commands": True
                    },
                    "smart_home": {
                        "enabled": SMART_HOME_AVAILABLE,
                        "config_file": "smart_home_config.json"
                    },
                    "gui": {
                        "enabled": GUI_AVAILABLE,
                        "theme": "light"
                    },
                    "voice_enhancements": {
                        "enabled": VOICE_ENHANCEMENTS_AVAILABLE,
                        "wake_word": {
                            "enabled": True,
                            "keywords": ["hey clover"],
                            "sensitivity": 0.5,
                            "access_key": ""
                        },
                        "tts": {
                            "engine": "best",
                            "voice_id": "",
                            "api_key": "",
                            "rate": 150,
                            "volume": 1.0,
                            "pitch": 1.0
                        }
                    }
                }

                with open("advanced_config.json", "w") as f:
                    json.dump(default_config, f, indent=4)

                return default_config
        except Exception as e:
            logger.error(f"Error loading advanced configuration: {e}")
            return {}

    def save_advanced_config(self):
        """Save advanced configuration"""
        try:
            with open("advanced_config.json", "w") as f:
                json.dump(self.advanced_config, f, indent=4)
            logger.info("Advanced configuration saved")
        except Exception as e:
            logger.error(f"Error saving advanced configuration: {e}")

    def initialize_advanced_features(self):
        """Initialize all available advanced features"""
        # Initialize wake word detection
        if (WAKE_WORD_AVAILABLE and
            self.advanced_config.get("wake_word", {}).get("enabled", False)):
            self.initialize_wake_word()

        # Initialize GPT integration
        if (GPT_AVAILABLE and
            self.advanced_config.get("gpt", {}).get("enabled", False)):
            self.initialize_gpt()

        # Initialize smart home control
        if (SMART_HOME_AVAILABLE and
            self.advanced_config.get("smart_home", {}).get("enabled", False)):
            self.initialize_smart_home()

        # Initialize voice enhancements
        if (VOICE_ENHANCEMENTS_AVAILABLE and
            self.advanced_config.get("voice_enhancements", {}).get("enabled", False)):
            self.initialize_voice_enhancements()

    def initialize_wake_word(self):
        """Initialize wake word detection"""
        try:
            wake_config = self.advanced_config.get("wake_word", {})
            keywords = wake_config.get("keywords", ["jarvis"])
            sensitivity = wake_config.get("sensitivity", 0.5)
            access_key = wake_config.get("access_key", "")

            if not access_key:
                logger.warning("Wake word detection requires an access key")
                return

            self.wake_word_detector = WakeWordDetector(
                keywords=keywords,
                access_key=access_key,
                sensitivity=sensitivity,
                callback=self.on_wake_word
            )

            if self.wake_word_detector.initialize():
                self.wake_word_detector.start()
                logger.info(f"Wake word detection started with keywords: {keywords}")
            else:
                logger.error("Failed to initialize wake word detection")
                self.wake_word_detector = None
        except Exception as e:
            logger.error(f"Error initializing wake word detection: {e}")
            self.wake_word_detector = None

    def initialize_gpt(self):
        """Initialize GPT integration"""
        try:
            gpt_config = self.advanced_config.get("gpt", {})
            api_key = gpt_config.get("api_key", "")
            model = gpt_config.get("model", "gpt-3.5-turbo")

            if not api_key:
                logger.warning("GPT integration requires an API key")
                return

            self.gpt_assistant = GPTAssistant(
                api_key=api_key,
                model=model
            )

            logger.info(f"GPT integration initialized with model: {model}")
        except Exception as e:
            logger.error(f"Error initializing GPT integration: {e}")
            self.gpt_assistant = None

    def initialize_smart_home(self):
        """Initialize smart home control"""
        try:
            smart_home_config = self.advanced_config.get("smart_home", {})
            config_file = smart_home_config.get("config_file", "smart_home_config.json")

            self.smart_home = SmartHomeController(config_file=config_file)

            # Discover devices
            devices = self.smart_home.get_all_devices()
            logger.info(f"Smart home control initialized with {len(devices)} devices")
        except Exception as e:
            logger.error(f"Error initializing smart home control: {e}")
            self.smart_home = None

    def initialize_voice_enhancements(self):
        """Initialize voice enhancements"""
        try:
            voice_config = self.advanced_config.get("voice_enhancements", {})

            # Create a voice enhancements instance
            self.voice_enhancements = VoiceEnhancements()

            # Configure wake word
            wake_word_config = voice_config.get("wake_word", {})
            if wake_word_config.get("enabled", True):
                # Update the wake word configuration
                self.voice_enhancements.config["wake_word"]["keywords"] = wake_word_config.get("keywords", ["clover"])
                self.voice_enhancements.config["wake_word"]["sensitivity"] = wake_word_config.get("sensitivity", 0.5)
                self.voice_enhancements.config["wake_word"]["access_key"] = wake_word_config.get("access_key", "")

                # Set the callback function
                self.voice_enhancements.set_wake_word_callback(self.on_wake_word)

            # Configure TTS
            tts_config = voice_config.get("tts", {})
            self.voice_enhancements.config["tts"]["engine"] = tts_config.get("engine", "best")
            self.voice_enhancements.config["tts"]["voice_id"] = tts_config.get("voice_id", "")
            self.voice_enhancements.config["tts"]["api_key"] = tts_config.get("api_key", "")
            self.voice_enhancements.config["tts"]["rate"] = tts_config.get("rate", 150)
            self.voice_enhancements.config["tts"]["volume"] = tts_config.get("volume", 1.0)
            self.voice_enhancements.config["tts"]["pitch"] = tts_config.get("pitch", 1.0)

            # Save the configuration
            self.voice_enhancements.save_config()

            # Re-initialize the enhancements with the updated configuration
            self.voice_enhancements.initialize_enhancements()

            # Start wake word detection if enabled
            if wake_word_config.get("enabled", True) and wake_word_config.get("access_key", ""):
                self.voice_enhancements.start_wake_word_detection()
                logger.info("Voice enhancements initialized with wake word detection")
            else:
                logger.info("Voice enhancements initialized without wake word detection")

            # Override the speak method to use the advanced TTS
            self._original_speak = self.speak
            def enhanced_speak(text):
                if self.voice_enhancements and self.voice_enhancements.tts_engine:
                    return self.voice_enhancements.speak(text)
                else:
                    return self._original_speak(text)
            self.speak = enhanced_speak

        except Exception as e:
            logger.error(f"Error initializing voice enhancements: {e}")
            self.voice_enhancements = None

    def on_wake_word(self, keyword):
        """Callback when wake word is detected"""
        logger.info(f"Wake word detected: {keyword}")
        self.speak("I'm listening")

        # Process a command
        query = self.take_command()
        if query:
            self.process_command(query)

    def add_advanced_commands(self):
        """Add commands for advanced features"""
        # Add GPT command if available
        if self.gpt_assistant:
            from enhanced_voice_assistant import Command

            class GPTCommand(Command):
                """Use GPT for natural language conversation"""
                def __init__(self, assistant):
                    super().__init__(assistant)

                def matches(self, query: str) -> bool:
                    # This is a fallback command, so it should match when no other command does
                    # The actual matching is done in the process_command method
                    return False

                def execute(self, query: str) -> bool:
                    response = self.assistant.gpt_assistant.get_response(query)
                    if response:
                        self.assistant.speak(response)
                        return True
                    return False

            # Add the GPT command to the end of the list
            self.commands.append(GPTCommand(self))

            # Also add a specific command to chat with GPT
            class ChatGPTCommand(Command):
                """Explicitly chat with GPT"""
                def matches(self, query: str) -> bool:
                    return "chat" in query and ("gpt" in query or "ai" in query)

                def execute(self, query: str) -> bool:
                    self.assistant.speak("What would you like to chat about?")
                    chat_query = self.assistant.take_command()
                    if chat_query:
                        response = self.assistant.gpt_assistant.get_response(chat_query)
                        if response:
                            self.assistant.speak(response)
                            return True
                    return False

            self.commands.append(ChatGPTCommand(self))

        # Add smart home commands if available
        if self.smart_home:
            from enhanced_voice_assistant import Command

            class SmartHomeCommand(Command):
                """Control smart home devices"""
                def matches(self, query: str) -> bool:
                    return ("turn" in query or "switch" in query or
                            "light" in query or "device" in query)

                def execute(self, query: str) -> bool:
                    # Extract device and command
                    device = None
                    command = None

                    # Check for "turn on/off" commands
                    if "turn on" in query or "switch on" in query:
                        command = "on"
                        # Extract device name (after "turn on" or "switch on")
                        if "turn on" in query:
                            device = query.split("turn on")[1].strip()
                        else:
                            device = query.split("switch on")[1].strip()
                    elif "turn off" in query or "switch off" in query:
                        command = "off"
                        # Extract device name (after "turn off" or "switch off")
                        if "turn off" in query:
                            device = query.split("turn off")[1].strip()
                        else:
                            device = query.split("switch off")[1].strip()

                    if not device or not command:
                        self.assistant.speak("I'm not sure which device you want to control")
                        return False

                    # Try to control the device
                    result = self.assistant.smart_home.control_device(device, command)

                    if result:
                        self.assistant.speak(f"Turned {command} {device}")
                        return True
                    else:
                        self.assistant.speak(f"I couldn't control {device}")
                        return False

            self.commands.append(SmartHomeCommand(self))

        # Add system control commands if available
        if SYSTEM_CONTROL_AVAILABLE:
            # Add all system commands
            system_commands = get_system_commands(self)
            for command in system_commands:
                self.commands.append(command)
            logger.info(f"Added {len(system_commands)} system control commands")

    def process_command(self, query: str) -> None:
        """Process user commands with advanced features"""
        try:
            # First try the base commands
            for command in self.commands[:-1]:  # Exclude the GPT fallback command
                if command.matches(query):
                    if command.execute(query):
                        return

            # If no command matched and GPT is enabled for unknown commands, use GPT
            if (self.gpt_assistant and
                self.advanced_config.get("gpt", {}).get("use_for_unknown_commands", True)):
                gpt_command = self.commands[-1]  # The GPT command should be the last one
                if gpt_command.execute(query):
                    return

            # If we get here, no command matched
            self.speak("I'm not sure how to help with that")

        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self.speak("Sorry, I encountered an error while processing your request")

    def run_with_gui(self):
        """Run the assistant with GUI"""
        if not GUI_AVAILABLE:
            logger.error("GUI is not available")
            return self.run()

        try:
            root = tk.Tk()
            self.gui = AssistantGUI(root)
            root.mainloop()
        except Exception as e:
            logger.error(f"Error running GUI: {e}")
            return self.run()

    def configure_advanced(self):
        """Configure advanced features"""
        self.speak("Let's configure the advanced features")

        # Configure wake word detection
        if WAKE_WORD_AVAILABLE:
            self.speak("Would you like to enable wake word detection?")
            response = self.take_command()
            if response and ("yes" in response.lower() or "sure" in response.lower()):
                self.advanced_config["wake_word"]["enabled"] = True

                self.speak("Please enter your Picovoice access key in the console")
                access_key = input("Picovoice access key: ")
                self.advanced_config["wake_word"]["access_key"] = access_key

                self.speak("What wake words would you like to use? Options include jarvis, computer, alexa, and others.")
                wake_word_response = self.take_command()
                if wake_word_response:
                    keywords = []
                    for keyword in get_available_keywords():
                        if keyword in wake_word_response.lower():
                            keywords.append(keyword)

                    if keywords:
                        self.advanced_config["wake_word"]["keywords"] = keywords
                        self.speak(f"Wake words set to: {', '.join(keywords)}")
                    else:
                        self.advanced_config["wake_word"]["keywords"] = ["jarvis"]
                        self.speak("Using default wake word: jarvis")
            else:
                self.advanced_config["wake_word"]["enabled"] = False

        # Configure GPT integration
        if GPT_AVAILABLE:
            self.speak("Would you like to enable GPT integration for more natural conversations?")
            response = self.take_command()
            if response and ("yes" in response.lower() or "sure" in response.lower()):
                self.advanced_config["gpt"]["enabled"] = True

                self.speak("Please enter your OpenAI API key in the console")
                api_key = input("OpenAI API key: ")
                self.advanced_config["gpt"]["api_key"] = api_key

                self.speak("Would you like to use GPT for commands that I don't understand?")
                fallback_response = self.take_command()
                if fallback_response:
                    self.advanced_config["gpt"]["use_for_unknown_commands"] = (
                        "yes" in fallback_response.lower() or
                        "sure" in fallback_response.lower()
                    )
            else:
                self.advanced_config["gpt"]["enabled"] = False

        # Configure smart home
        if SMART_HOME_AVAILABLE:
            self.speak("Would you like to enable smart home control?")
            response = self.take_command()
            if response and ("yes" in response.lower() or "sure" in response.lower()):
                self.advanced_config["smart_home"]["enabled"] = True
                self.speak("Smart home control enabled. You'll need to configure your devices in the smart home configuration file.")
            else:
                self.advanced_config["smart_home"]["enabled"] = False

        # Configure voice enhancements
        if VOICE_ENHANCEMENTS_AVAILABLE:
            self.speak("Would you like to enable voice enhancements?")
            response = self.take_command()
            if response and ("yes" in response.lower() or "sure" in response.lower()):
                self.advanced_config["voice_enhancements"]["enabled"] = True

                # Configure wake word
                self.speak("Would you like to use Hey Clover as your wake word?")
                wake_word_response = self.take_command()
                if wake_word_response and ("yes" in wake_word_response.lower() or "sure" in wake_word_response.lower()):
                    self.advanced_config["voice_enhancements"]["wake_word"]["enabled"] = True
                    self.advanced_config["voice_enhancements"]["wake_word"]["keywords"] = ["hey clover"]

                    self.speak("Please enter your Picovoice access key in the console")
                    access_key = input("Picovoice access key: ")
                    if access_key:
                        self.advanced_config["voice_enhancements"]["wake_word"]["access_key"] = access_key
                else:
                    self.advanced_config["voice_enhancements"]["wake_word"]["enabled"] = False

                # Configure TTS
                self.speak("Would you like to use a more natural-sounding voice?")
                tts_response = self.take_command()
                if tts_response and ("yes" in tts_response.lower() or "sure" in tts_response.lower()):
                    self.speak("Which TTS engine would you prefer? Options are: best quality, Google, Microsoft Edge, or basic.")
                    engine_response = self.take_command()

                    if engine_response:
                        if "best" in engine_response.lower() or "quality" in engine_response.lower():
                            self.advanced_config["voice_enhancements"]["tts"]["engine"] = "best"

                            self.speak("For the best quality voice, please enter your ElevenLabs API key in the console")
                            api_key = input("ElevenLabs API key: ")
                            if api_key:
                                self.advanced_config["voice_enhancements"]["tts"]["api_key"] = api_key

                        elif "google" in engine_response.lower():
                            self.advanced_config["voice_enhancements"]["tts"]["engine"] = "gtts"

                        elif "microsoft" in engine_response.lower() or "edge" in engine_response.lower():
                            self.advanced_config["voice_enhancements"]["tts"]["engine"] = "edge"

                        else:
                            self.advanced_config["voice_enhancements"]["tts"]["engine"] = "pyttsx3"

                    self.speak(f"Voice set to {self.advanced_config['voice_enhancements']['tts']['engine']}")
                else:
                    self.advanced_config["voice_enhancements"]["tts"]["engine"] = "pyttsx3"
            else:
                self.advanced_config["voice_enhancements"]["enabled"] = False

        # Save the configuration
        self.save_advanced_config()

        # Initialize the features
        self.initialize_advanced_features()

        self.speak("Advanced configuration complete")

def main():
    """Main function"""
    print("=" * 50)
    print("Advanced Voice Assistant")
    print("=" * 50)

    try:
        assistant = AdvancedVoiceAssistant()

        # Check if this is the first run or if configuration is incomplete
        if (not assistant.advanced_config.get("wake_word", {}).get("access_key") and WAKE_WORD_AVAILABLE or
            not assistant.advanced_config.get("gpt", {}).get("api_key") and GPT_AVAILABLE):
            print("It looks like some advanced features are not configured.")
            assistant.speak("Would you like to configure the advanced features now?")
            response = assistant.take_command()
            if response and ("yes" in response.lower() or "sure" in response.lower()):
                assistant.configure_advanced()

        # Run with GUI if available and enabled
        if (GUI_AVAILABLE and
            assistant.advanced_config.get("gui", {}).get("enabled", True)):
            assistant.run_with_gui()
        else:
            assistant.run()
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        print(f"Critical error: {e}")

if __name__ == "__main__":
    main()
