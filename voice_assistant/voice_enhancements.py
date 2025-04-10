"""
Voice Assistant Enhancements
--------------------------
This module integrates the custom wake word and advanced TTS features.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List

# Import custom modules
from custom_wake_word import CustomWakeWordDetector, create_custom_wake_word_detector
from advanced_tts import AdvancedTTS, create_best_tts_engine, TTSEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VoiceEnhancements:
    """
    Class to manage voice assistant enhancements
    """
    def __init__(self, config_file: str = "voice_enhancements.json"):
        """
        Initialize voice enhancements.

        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.config = self.load_config()

        self.wake_word_detector = None
        self.tts_engine = None

        # Initialize enhancements
        self.initialize_enhancements()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                # Create default configuration
                default_config = {
                    "wake_word": {
                        "enabled": True,
                        "keywords": ["hey clover"],
                        "sensitivity": 0.5,
                        "access_key": ""
                    },
                    "tts": {
                        "engine": "pyttsx3",  # pyttsx3, gtts, edge, elevenlabs
                        "voice_id": "",
                        "api_key": "",
                        "rate": 150,
                        "volume": 1.0,
                        "pitch": 1.0,
                        "language": "en"  # en, hi, etc.
                    }
                }

                # Save default configuration
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=4)

                return default_config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return {
                "wake_word": {"enabled": False},
                "tts": {"engine": "pyttsx3"}
            }

    def save_config(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")

    def initialize_enhancements(self) -> None:
        """Initialize voice enhancements"""
        # Initialize wake word detection
        self.initialize_wake_word()

        # Initialize TTS engine
        self.initialize_tts()

    def initialize_wake_word(self) -> None:
        """Initialize custom wake word detection"""
        try:
            if not self.config["wake_word"]["enabled"]:
                logger.info("Wake word detection is disabled")
                return

            keywords = self.config["wake_word"]["keywords"]
            sensitivity = self.config["wake_word"]["sensitivity"]
            access_key = self.config["wake_word"]["access_key"]

            if not access_key:
                logger.warning("Wake word detection requires an access key")
                return

            # Create the wake word detector
            self.wake_word_detector = create_custom_wake_word_detector(
                keywords=keywords,
                access_key=access_key,
                sensitivity=sensitivity,
                callback=None  # Will be set by the caller
            )

            if self.wake_word_detector:
                logger.info(f"Custom wake word detector initialized with keywords: {keywords}")
            else:
                logger.error("Failed to initialize custom wake word detector")
        except Exception as e:
            logger.error(f"Error initializing wake word detection: {e}")

    def initialize_tts(self) -> None:
        """Initialize advanced TTS engine"""
        try:
            engine = self.config["tts"]["engine"]
            voice_id = self.config["tts"]["voice_id"]
            api_key = self.config["tts"]["api_key"]
            rate = self.config["tts"]["rate"]
            volume = self.config["tts"]["volume"]
            pitch = self.config["tts"]["pitch"]

            # Get language setting (default to English)
            language = self.config["tts"].get("language", "en")

            # Create the TTS engine
            if engine == "best":
                self.tts_engine = create_best_tts_engine(api_key=api_key)
            elif engine == "hindi":
                self.tts_engine = create_best_tts_engine(api_key=api_key, use_hindi=True)
            else:
                self.tts_engine = AdvancedTTS(
                    engine=engine,
                    voice_id=voice_id,
                    api_key=api_key,
                    rate=rate,
                    volume=volume,
                    pitch=pitch,
                    language=language
                )

            logger.info(f"Advanced TTS engine initialized with engine: {engine}")
        except Exception as e:
            logger.error(f"Error initializing TTS engine: {e}")
            # Fallback to basic TTS
            self.tts_engine = AdvancedTTS(engine=TTSEngine.PYTTSX3)

    def set_wake_word_callback(self, callback) -> None:
        """
        Set the callback function for wake word detection.

        Args:
            callback: Function to call when wake word is detected
        """
        if self.wake_word_detector:
            self.wake_word_detector.callback = callback
            logger.info("Wake word callback set")

    def start_wake_word_detection(self) -> bool:
        """
        Start wake word detection.

        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.wake_word_detector:
            return self.wake_word_detector.start()
        return False

    def stop_wake_word_detection(self) -> None:
        """Stop wake word detection"""
        if self.wake_word_detector:
            self.wake_word_detector.stop()

    def speak(self, text: str) -> bool:
        """
        Convert text to speech using the advanced TTS engine.

        Args:
            text: Text to convert to speech

        Returns:
            bool: True if successful, False otherwise
        """
        if self.tts_engine:
            return self.tts_engine.speak(text)
        return False

    def get_available_voices(self) -> List[Dict[str, Any]]:
        """
        Get a list of available voices for the current TTS engine.

        Returns:
            list: List of available voices
        """
        if self.tts_engine:
            return self.tts_engine.get_available_voices()
        return []

    def set_voice(self, voice_id: str) -> bool:
        """
        Set the voice to use for speech synthesis.

        Args:
            voice_id: ID of the voice to use

        Returns:
            bool: True if successful, False otherwise
        """
        if self.tts_engine:
            result = self.tts_engine.set_voice(voice_id)
            if result:
                self.config["tts"]["voice_id"] = voice_id
                self.save_config()
            return result
        return False

    def set_tts_engine(self, engine: str, api_key: Optional[str] = None) -> bool:
        """
        Set the TTS engine to use.

        Args:
            engine: TTS engine to use (pyttsx3, gtts, edge, elevenlabs, best)
            api_key: API key for online TTS services

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.config["tts"]["engine"] = engine
            if api_key:
                self.config["tts"]["api_key"] = api_key

            self.save_config()

            # Re-initialize the TTS engine
            self.initialize_tts()

            return True
        except Exception as e:
            logger.error(f"Error setting TTS engine: {e}")
            return False

    def set_wake_words(self, keywords: List[str]) -> bool:
        """
        Set the wake words to use.

        Args:
            keywords: List of wake words to use

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.config["wake_word"]["keywords"] = keywords
            self.save_config()

            # Re-initialize the wake word detector
            self.initialize_wake_word()

            return True
        except Exception as e:
            logger.error(f"Error setting wake words: {e}")
            return False

    def configure_interactive(self) -> None:
        """Interactive configuration of voice enhancements"""
        print("\n=== Voice Enhancements Configuration ===")

        # Configure wake word
        print("\n--- Wake Word Configuration ---")
        enable_wake_word = input("Enable wake word detection? (y/n): ").lower() == 'y'
        self.config["wake_word"]["enabled"] = enable_wake_word

        if enable_wake_word:
            keywords = input("Enter wake words (comma-separated, default: hey clover): ").strip()
            if keywords:
                self.config["wake_word"]["keywords"] = [k.strip() for k in keywords.split(',')]

            sensitivity = input("Enter sensitivity (0.0-1.0, default: 0.5): ").strip()
            if sensitivity:
                try:
                    self.config["wake_word"]["sensitivity"] = float(sensitivity)
                except ValueError:
                    print("Invalid sensitivity value, using default (0.5)")

            access_key = input("Enter Picovoice access key: ").strip()
            if access_key:
                self.config["wake_word"]["access_key"] = access_key

        # Configure TTS
        print("\n--- TTS Configuration ---")
        print("Available TTS engines:")
        print("1. pyttsx3 (offline, basic quality)")
        print("2. Google TTS (online, decent quality)")
        print("3. Microsoft Edge TTS (online, good quality)")
        print("4. ElevenLabs (online, premium quality)")
        print("5. Best available (tries in order: ElevenLabs > Edge > Google > pyttsx3)")
        print("6. Hindi voice (using Google TTS)")

        engine_choice = input("Select TTS engine (1-6, default: 1): ").strip()
        engine_map = {
            '1': 'pyttsx3',
            '2': 'gtts',
            '3': 'edge',
            '4': 'elevenlabs',
            '5': 'best',
            '6': 'gtts'  # Use gtts for Hindi
        }

        if engine_choice in engine_map:
            self.config["tts"]["engine"] = engine_map[engine_choice]

            # Set language to Hindi if option 6 was selected
            if engine_choice == '6':
                self.config["tts"]["language"] = "hi"
                print("Language set to Hindi")
            else:
                # Ask for language preference
                language_choice = input("Select language (en for English, hi for Hindi, default: en): ").strip().lower()
                if language_choice in ['en', 'hi']:
                    self.config["tts"]["language"] = language_choice
                    print(f"Language set to {language_choice}")

        if self.config["tts"]["engine"] in ['elevenlabs', 'best']:
            api_key = input("Enter ElevenLabs API key: ").strip()
            if api_key:
                self.config["tts"]["api_key"] = api_key

        # Save configuration
        self.save_config()
        print(f"\nConfiguration saved to {self.config_file}")

        # Re-initialize enhancements
        self.initialize_enhancements()

# Example usage
if __name__ == "__main__":
    def on_wake_word(keyword):
        print(f"Wake word detected: {keyword}")
        enhancements.speak(f"Yes, I heard you say {keyword}. How can I help?")

    # Create voice enhancements
    enhancements = VoiceEnhancements()

    # Configure interactively
    enhancements.configure_interactive()

    # Set wake word callback
    enhancements.set_wake_word_callback(on_wake_word)

    # Start wake word detection
    if enhancements.start_wake_word_detection():
        print("Say the wake word to test...")

        try:
            # Keep the program running
            while True:
                cmd = input("Press Enter to exit...")
                if cmd == '':
                    break
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            enhancements.stop_wake_word_detection()
    else:
        print("Failed to start wake word detection")

        # Test TTS
        print("Testing TTS...")
        enhancements.speak("Hello! I am your voice assistant with enhanced speech capabilities.")
