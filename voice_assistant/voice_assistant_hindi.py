"""
Hindi Voice Assistant
-------------------
This script runs the voice assistant with Hindi voice.
"""

import os
import sys
import logging
import background_assistant
from advanced_tts import create_best_tts_engine, TTSEngine
from voice_enhancements import VoiceEnhancements

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("hindi_assistant.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HindiVoiceAssistant:
    """
    Voice Assistant with Hindi voice
    """
    def __init__(self):
        """Initialize the Hindi voice assistant"""
        # Create a voice enhancements instance with Hindi voice
        self.voice_enhancements = VoiceEnhancements()

        # Load configuration
        self.voice_enhancements.load_config()

        # Update configuration for Hindi voice
        self.voice_enhancements.config["tts"]["engine"] = "gtts"

        # Add Hindi language setting
        if "language" not in self.voice_enhancements.config["tts"]:
            self.voice_enhancements.config["tts"]["language"] = "hi"
        else:
            self.voice_enhancements.config["tts"]["language"] = "hi"

        # Save the updated configuration
        self.voice_enhancements.save_config()

        # Initialize the voice enhancements
        self.voice_enhancements.initialize_enhancements()

        # Create the background assistant
        self.assistant = background_assistant.BackgroundAssistant()

        # Override the assistant's voice enhancements
        self.assistant.assistant.voice_enhancements = self.voice_enhancements

        logger.info("Hindi voice assistant initialized")

    def run(self):
        """Run the Hindi voice assistant"""
        try:
            # Start the assistant
            self.assistant.start_assistant()

            # Keep the main thread alive
            try:
                while True:
                    import time
                    time.sleep(1.0)
            except KeyboardInterrupt:
                self.assistant.exit_application()

        except Exception as e:
            logger.error(f"Error running Hindi voice assistant: {e}")

def main():
    """Main function"""
    print("Starting Hindi Voice Assistant...")
    print("Say 'Jarvis' to activate the assistant")
    print("The assistant will respond in Hindi")

    # Create and run the Hindi voice assistant
    assistant = HindiVoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
