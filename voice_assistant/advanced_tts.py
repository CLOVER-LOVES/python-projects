"""
Advanced Text-to-Speech Module
----------------------------
This module provides more natural-sounding voice synthesis using various TTS engines.
"""

import os
import io
import time
import tempfile
import logging
import threading
import pygame
import pyttsx3
from typing import Optional, Dict, List, Any, Union
from enum import Enum

# Try to import optional TTS engines
try:
    import gtts
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    import elevenlabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TTSEngine(Enum):
    """Enum for available TTS engines"""
    PYTTSX3 = "pyttsx3"  # Default, offline
    GTTS = "gtts"        # Google Text-to-Speech, online
    EDGE_TTS = "edge"    # Microsoft Edge TTS, online
    ELEVENLABS = "elevenlabs"  # ElevenLabs, online, high quality
    HINDI = "hindi"      # Hindi voice (using Google TTS)

class AdvancedTTS:
    """
    Advanced Text-to-Speech with multiple engine options
    """
    def __init__(self,
                 engine: Union[TTSEngine, str] = TTSEngine.PYTTSX3,
                 voice_id: Optional[str] = None,
                 api_key: Optional[str] = None,
                 rate: int = 150,
                 volume: float = 1.0,
                 pitch: float = 1.0,
                 language: str = 'en'):
        """
        Initialize the advanced TTS engine.

        Args:
            engine: TTS engine to use
            voice_id: Voice ID for the selected engine
            api_key: API key for online TTS services
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
            pitch: Voice pitch (0.5 to 2.0)
        """
        # Convert string to enum if needed
        if isinstance(engine, str):
            try:
                self.engine_type = TTSEngine(engine.lower())
            except ValueError:
                logger.warning(f"Unknown engine type: {engine}. Using default.")
                self.engine_type = TTSEngine.PYTTSX3
        else:
            self.engine_type = engine

        self.voice_id = voice_id
        self.api_key = api_key
        self.rate = rate
        self.volume = volume
        self.pitch = pitch
        self.language = language

        # Initialize pygame for audio playback
        pygame.mixer.init()

        # Initialize the selected engine
        self._initialize_engine()

    def _initialize_engine(self) -> None:
        """Initialize the selected TTS engine"""
        try:
            if self.engine_type == TTSEngine.PYTTSX3:
                self.engine = pyttsx3.init()

                # Set properties
                self.engine.setProperty('rate', self.rate)
                self.engine.setProperty('volume', self.volume)

                # Set voice if specified
                if self.voice_id:
                    self.engine.setProperty('voice', self.voice_id)
                # Otherwise use the first available voice
                else:
                    voices = self.engine.getProperty('voices')
                    if voices:
                        self.engine.setProperty('voice', voices[0].id)
                        self.voice_id = voices[0].id

                logger.info(f"Initialized pyttsx3 TTS engine with voice: {self.voice_id}")

            elif self.engine_type == TTSEngine.GTTS and GTTS_AVAILABLE:
                # Google TTS doesn't need initialization, just check if it's available
                logger.info("Initialized Google TTS engine")

            elif self.engine_type == TTSEngine.EDGE_TTS and EDGE_TTS_AVAILABLE:
                # Edge TTS doesn't need initialization, just check if it's available
                logger.info("Initialized Microsoft Edge TTS engine")

                # Set default voice if not specified
                if not self.voice_id:
                    self.voice_id = "en-US-AriaNeural"

            elif self.engine_type == TTSEngine.ELEVENLABS and ELEVENLABS_AVAILABLE:
                # Set API key for ElevenLabs
                if self.api_key:
                    elevenlabs.set_api_key(self.api_key)

                    # Set default voice if not specified
                    if not self.voice_id:
                        # Use the first available voice
                        voices = elevenlabs.voices()
                        if voices:
                            self.voice_id = voices[0].voice_id

                    logger.info(f"Initialized ElevenLabs TTS engine with voice: {self.voice_id}")
                else:
                    logger.warning("ElevenLabs API key not provided. Falling back to pyttsx3.")
                    self.engine_type = TTSEngine.PYTTSX3
                    self._initialize_engine()

            elif self.engine_type == TTSEngine.HINDI:
                # For Hindi voice, we'll use Google TTS with Hindi language
                if GTTS_AVAILABLE:
                    logger.info("Initialized Hindi voice using Google TTS")
                    # No specific initialization needed for gTTS
                else:
                    logger.warning("Google TTS not available for Hindi voice. Falling back to pyttsx3.")
                    self.engine_type = TTSEngine.PYTTSX3
                    self._initialize_engine()

            else:
                # Fallback to pyttsx3 if the selected engine is not available
                logger.warning(f"{self.engine_type.value} is not available. Falling back to pyttsx3.")
                self.engine_type = TTSEngine.PYTTSX3
                self._initialize_engine()

        except Exception as e:
            logger.error(f"Error initializing TTS engine: {e}")
            # Fallback to pyttsx3 if there's an error
            if self.engine_type != TTSEngine.PYTTSX3:
                logger.warning("Falling back to pyttsx3.")
                self.engine_type = TTSEngine.PYTTSX3
                self._initialize_engine()

    def speak(self, text: str) -> bool:
        """
        Convert text to speech using the selected engine.

        Args:
            text: Text to convert to speech

        Returns:
            bool: True if successful, False otherwise
        """
        if not text:
            return False

        try:
            if self.engine_type == TTSEngine.PYTTSX3:
                # Use pyttsx3
                self.engine.say(text)
                self.engine.runAndWait()
                return True

            elif self.engine_type == TTSEngine.GTTS and GTTS_AVAILABLE:
                # Use Google TTS
                tts = gtts.gTTS(text=text, lang=self.language, slow=False)

                # Save to a temporary file and play
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_file = fp.name

                tts.save(temp_file)
                self._play_audio(temp_file)

                # Clean up the temporary file
                try:
                    os.unlink(temp_file)
                except:
                    pass

                return True

            elif self.engine_type == TTSEngine.EDGE_TTS and EDGE_TTS_AVAILABLE:
                # Use Microsoft Edge TTS
                communicate = edge_tts.Communicate(text, self.voice_id)

                # Save to a temporary file and play
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_file = fp.name

                # Run the async function in a synchronous context
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(communicate.save(temp_file))
                finally:
                    loop.close()

                self._play_audio(temp_file)

                # Clean up the temporary file
                try:
                    os.unlink(temp_file)
                except:
                    pass

                return True

            elif self.engine_type == TTSEngine.ELEVENLABS and ELEVENLABS_AVAILABLE:
                # Use ElevenLabs
                audio = elevenlabs.generate(
                    text=text,
                    voice=self.voice_id,
                    model="eleven_monolingual_v1"
                )

                # Save to a temporary file and play
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_file = fp.name
                    fp.write(audio)

                self._play_audio(temp_file)

                # Clean up the temporary file
                try:
                    os.unlink(temp_file)
                except:
                    pass

                return True

            elif self.engine_type == TTSEngine.HINDI and GTTS_AVAILABLE:
                # Use Google TTS with Hindi language
                try:
                    # Create a gTTS object with Hindi language
                    tts = gtts.gTTS(text=text, lang='hi', slow=False)

                    # Save to a temporary file
                    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as fp:
                        tts.save(fp.name)
                        temp_file = fp.name

                    # Play the audio
                    self._play_audio(temp_file)

                    # Clean up the temporary file
                    try:
                        os.unlink(temp_file)
                    except:
                        pass

                    return True
                except Exception as e:
                    logger.error(f"Error using Hindi voice: {e}")
                    # Fallback to pyttsx3
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()
                    return True

            else:
                logger.error(f"Unknown TTS engine: {self.engine_type}")
                return False

        except Exception as e:
            logger.error(f"Error in speech synthesis: {e}")

            # Try fallback to pyttsx3 if another engine fails
            if self.engine_type != TTSEngine.PYTTSX3:
                logger.warning("Falling back to pyttsx3 for this speech.")
                try:
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()
                    return True
                except Exception as e2:
                    logger.error(f"Fallback speech synthesis also failed: {e2}")

            return False

    def _play_audio(self, file_path: str) -> None:
        """
        Play an audio file using pygame.

        Args:
            file_path: Path to the audio file
        """
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            logger.error(f"Error playing audio: {e}")

    def get_available_voices(self) -> List[Dict[str, Any]]:
        """
        Get a list of available voices for the current engine.

        Returns:
            list: List of available voices
        """
        voices = []

        try:
            if self.engine_type == TTSEngine.PYTTSX3:
                # Get pyttsx3 voices
                for voice in self.engine.getProperty('voices'):
                    voices.append({
                        'id': voice.id,
                        'name': voice.name,
                        'languages': voice.languages,
                        'gender': voice.gender,
                        'age': voice.age
                    })

            elif self.engine_type == TTSEngine.EDGE_TTS and EDGE_TTS_AVAILABLE:
                # Get Edge TTS voices
                # This requires running an async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    voice_list = loop.run_until_complete(edge_tts.list_voices())
                    for voice in voice_list:
                        voices.append({
                            'id': voice["ShortName"],
                            'name': voice["FriendlyName"],
                            'locale': voice["Locale"],
                            'gender': voice["Gender"],
                            'engine': 'edge'
                        })
                finally:
                    loop.close()

            elif self.engine_type == TTSEngine.ELEVENLABS and ELEVENLABS_AVAILABLE:
                # Get ElevenLabs voices
                voice_list = elevenlabs.voices()
                for voice in voice_list:
                    voices.append({
                        'id': voice.voice_id,
                        'name': voice.name,
                        'description': voice.description,
                        'engine': 'elevenlabs'
                    })

        except Exception as e:
            logger.error(f"Error getting available voices: {e}")

        return voices

    def set_voice(self, voice_id: str) -> bool:
        """
        Set the voice to use for speech synthesis.

        Args:
            voice_id: ID of the voice to use

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.voice_id = voice_id

            if self.engine_type == TTSEngine.PYTTSX3:
                self.engine.setProperty('voice', voice_id)

            logger.info(f"Voice set to: {voice_id}")
            return True

        except Exception as e:
            logger.error(f"Error setting voice: {e}")
            return False

    def set_rate(self, rate: int) -> bool:
        """
        Set the speech rate.

        Args:
            rate: Speech rate (words per minute)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.rate = rate

            if self.engine_type == TTSEngine.PYTTSX3:
                self.engine.setProperty('rate', rate)

            logger.info(f"Speech rate set to: {rate}")
            return True

        except Exception as e:
            logger.error(f"Error setting speech rate: {e}")
            return False

    def set_volume(self, volume: float) -> bool:
        """
        Set the speech volume.

        Args:
            volume: Volume level (0.0 to 1.0)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.volume = max(0.0, min(1.0, volume))  # Ensure volume is between 0.0 and 1.0

            if self.engine_type == TTSEngine.PYTTSX3:
                self.engine.setProperty('volume', self.volume)

            # For other engines, we'll adjust the pygame volume
            pygame.mixer.music.set_volume(self.volume)

            logger.info(f"Speech volume set to: {self.volume}")
            return True

        except Exception as e:
            logger.error(f"Error setting speech volume: {e}")
            return False

# Function to create an advanced TTS engine with the best available quality
def create_best_tts_engine(api_key: Optional[str] = None, use_hindi: bool = False) -> AdvancedTTS:
    """
    Create the best available TTS engine based on installed packages.

    Args:
        api_key: API key for online TTS services (ElevenLabs)
        use_hindi: Whether to use Hindi voice

    Returns:
        AdvancedTTS: The best available TTS engine
    """
    # If Hindi voice is requested, use Google TTS with Hindi language
    if use_hindi and GTTS_AVAILABLE:
        try:
            tts = AdvancedTTS(engine=TTSEngine.HINDI)
            logger.info("Using Hindi voice with Google TTS")
            return tts
        except Exception as e:
            logger.warning(f"Failed to initialize Hindi voice: {e}")

    # Try ElevenLabs first (highest quality)
    if ELEVENLABS_AVAILABLE and api_key:
        try:
            tts = AdvancedTTS(engine=TTSEngine.ELEVENLABS, api_key=api_key)
            logger.info("Using ElevenLabs TTS engine (highest quality)")
            return tts
        except Exception as e:
            logger.warning(f"Failed to initialize ElevenLabs TTS: {e}")

    # Try Edge TTS next
    if EDGE_TTS_AVAILABLE:
        try:
            tts = AdvancedTTS(engine=TTSEngine.EDGE_TTS)
            logger.info("Using Microsoft Edge TTS engine (good quality)")
            return tts
        except Exception as e:
            logger.warning(f"Failed to initialize Edge TTS: {e}")

    # Try Google TTS next
    if GTTS_AVAILABLE:
        try:
            tts = AdvancedTTS(engine=TTSEngine.GTTS)
            logger.info("Using Google TTS engine (decent quality)")
            return tts
        except Exception as e:
            logger.warning(f"Failed to initialize Google TTS: {e}")

    # Fallback to pyttsx3
    logger.info("Using pyttsx3 TTS engine (basic quality)")
    return AdvancedTTS(engine=TTSEngine.PYTTSX3)

# Example usage
if __name__ == "__main__":
    # Create the best available TTS engine
    tts = create_best_tts_engine()

    # List available voices
    voices = tts.get_available_voices()
    print(f"Available voices ({len(voices)}):")
    for i, voice in enumerate(voices[:5]):  # Show first 5 voices
        print(f"{i+1}. {voice.get('name', 'Unknown')} ({voice.get('id', 'Unknown')})")

    # Speak some text
    tts.speak("Hello! I am your advanced voice assistant with a more natural-sounding voice.")
