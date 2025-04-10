"""
Voice Assistant - Main Entry Point
---------------------------------
This file serves as the main entry point for the Voice Assistant application.
Run this file to start the voice assistant.
"""

from enhanced_voice_assistant import VoiceAssistant

if __name__ == "__main__":
    print("Starting Voice Assistant...")
    print("=" * 50)
    print("Enhanced Voice Assistant v1.0")
    print("Say 'exit' or 'quit' to end the session")
    print("=" * 50)
    
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nVoice Assistant stopped by user")
    except Exception as e:
        print(f"\nCritical error: {e}")
        print("Voice Assistant has stopped due to an error")
    finally:
        print("\nThank you for using Voice Assistant!")
