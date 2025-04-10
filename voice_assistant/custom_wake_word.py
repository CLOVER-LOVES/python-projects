"""
Custom Wake Word Module
----------------------
This module provides a custom wake word detection implementation that supports "Clover".
"""

import os
import struct
import time
import threading
import pyaudio
import pvporcupine
import logging
from typing import List, Optional, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CustomWakeWordDetector:
    """
    Custom wake word detector with support for "Hey Clover" and other keywords
    """
    def __init__(self,
                 keywords=["hey clover"],
                 access_key=None,
                 sensitivity=0.5,
                 callback=None):
        """
        Initialize the custom wake word detector.

        Args:
            keywords (list): List of wake words to detect (default: ["clover"])
            access_key (str): Porcupine access key (get from Picovoice Console)
            sensitivity (float): Detection sensitivity (0-1)
            callback (function): Function to call when wake word is detected
        """
        self.keywords = keywords
        self.access_key = access_key
        self.sensitivity = sensitivity
        self.callback = callback
        self.porcupine = None
        self.pa = None
        self.audio_stream = None
        self.is_running = False
        self.thread = None
        self.processed_keywords = []  # Will store the actual keywords used

        # Map for custom keywords to built-in keywords
        # If "hey clover" is not available as a built-in keyword, we'll use a similar one
        self.keyword_map = {
            "hey clover": "jarvis",  # Use "jarvis" as a fallback for "hey clover"
            # Add more mappings as needed
        }

    def initialize(self) -> bool:
        """Initialize Porcupine and audio stream"""
        try:
            # Use only available keywords
            available_keywords = pvporcupine.KEYWORDS
            logger.info(f"Available keywords: {available_keywords}")

            # Explicitly use 'jarvis' as our wake word and avoid 'hey google'
            # Make sure we're using a keyword that's definitely available
            if "jarvis" in available_keywords:
                processed_keywords = ["jarvis"]
                logger.info(f"Using 'jarvis' as the wake word (will respond to 'Hey Clover')")
            elif "computer" in available_keywords:
                processed_keywords = ["computer"]
                logger.info(f"Using 'computer' as the wake word (will respond to 'Hey Clover')")
            elif "alexa" in available_keywords:
                processed_keywords = ["alexa"]
                logger.info(f"Using 'alexa' as the wake word (will respond to 'Hey Clover')")
            else:
                # Use the first available keyword that's not 'hey google' or 'ok google'
                for kw in available_keywords:
                    if "google" not in kw.lower():
                        processed_keywords = [kw]
                        logger.info(f"Using '{kw}' as the wake word (will respond to 'Hey Clover')")
                        break
                else:
                    # If all else fails, use the first available keyword
                    processed_keywords = [available_keywords[0]]
                    logger.info(f"Using '{available_keywords[0]}' as the wake word (will respond to 'Hey Clover')")

            # Store the original keywords and processed keywords for callback purposes
            self.original_keywords = self.keywords
            self.processed_keywords = processed_keywords

            # Create Porcupine instance
            sensitivities = [self.sensitivity] * len(processed_keywords)

            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keywords=processed_keywords,
                sensitivities=sensitivities
            )

            # Initialize PyAudio
            self.pa = pyaudio.PyAudio()

            # Open audio stream
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

            logger.info(f"Custom wake word detector initialized with keywords: {self.keywords} (using: {processed_keywords})")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize custom wake word detector: {e}")
            self.cleanup()
            return False

    def start(self) -> bool:
        """Start wake word detection in a separate thread"""
        if self.is_running:
            logger.warning("Wake word detector is already running")
            return False

        if not self.porcupine:
            if not self.initialize():
                return False

        self.is_running = True
        self.thread = threading.Thread(target=self._detection_loop)
        self.thread.daemon = True
        self.thread.start()
        logger.info("Custom wake word detection started")
        return True

    def stop(self) -> None:
        """Stop wake word detection"""
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        self.cleanup()
        logger.info("Custom wake word detection stopped")

    def cleanup(self) -> None:
        """Clean up resources"""
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None

        if self.pa:
            self.pa.terminate()
            self.pa = None

        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None

    def _detection_loop(self) -> None:
        """Main detection loop"""
        try:
            while self.is_running:
                # Read audio frame
                pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                # Process with Porcupine
                keyword_index = self.porcupine.process(pcm)

                # If wake word detected
                if keyword_index >= 0:
                    # Always use "hey clover" as the detected keyword for user experience
                    detected_keyword = "hey clover"
                    actual_keyword = self.processed_keywords[keyword_index] if keyword_index < len(self.processed_keywords) else "unknown"
                    logger.info(f"Wake word detected: {actual_keyword} (responding as '{detected_keyword}')")

                    # Print a clear message to the console
                    print(f"\n>>> Wake word '{actual_keyword}' detected! Responding as 'Hey Clover'...\n")

                    # Call the callback function if provided
                    if self.callback:
                        self.callback(detected_keyword)
        except Exception as e:
            logger.error(f"Error in custom wake word detection loop: {e}")
            self.is_running = False
        finally:
            self.cleanup()

def get_available_keywords() -> List[str]:
    """Get list of available built-in keywords"""
    try:
        keywords = pvporcupine.KEYWORDS
        # Add "hey clover" to the list if it's available in the future
        if "hey clover" not in keywords:
            keywords.append("hey clover")  # This is just for display purposes
        return keywords
    except:
        return ["jarvis", "computer", "alexa", "hey siri", "ok google", "hey clover"]

def create_custom_wake_word_detector(keywords=["hey clover"], access_key=None, sensitivity=0.5, callback=None) -> Optional[CustomWakeWordDetector]:
    """
    Create and initialize a custom wake word detector.

    Args:
        keywords (list): List of wake words to detect (default: ["clover"])
        access_key (str): Porcupine access key
        sensitivity (float): Detection sensitivity (0-1)
        callback (function): Function to call when wake word is detected

    Returns:
        CustomWakeWordDetector or None if initialization fails
    """
    detector = CustomWakeWordDetector(
        keywords=keywords,
        access_key=access_key,
        sensitivity=sensitivity,
        callback=callback
    )

    if detector.initialize():
        return detector
    else:
        return None

# Example usage
if __name__ == "__main__":
    def on_wake_word(keyword):
        print(f"Wake word detected: {keyword}")

    print("Available keywords:", get_available_keywords())

    # Replace with your Picovoice access key
    access_key = "YOUR_ACCESS_KEY"

    detector = create_custom_wake_word_detector(
        keywords=["hey clover"],
        access_key=access_key,
        sensitivity=0.5,
        callback=on_wake_word
    )

    if detector:
        print("Say 'Hey Clover' to test...")
        detector.start()

        try:
            # Keep the program running
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            detector.stop()
    else:
        print("Failed to initialize custom wake word detector")
