import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Get all available voices
voices = engine.getProperty('voices')

# Print all voices with their details
print("Available voices:")
print("-" * 50)
for i, voice in enumerate(voices):
    print(f"Voice #{i+1}:")
    print(f"  ID: {voice.id}")
    print(f"  Name: {voice.name}")
    print(f"  Languages: {voice.languages}")
    print(f"  Gender: {voice.gender}")
    print(f"  Age: {voice.age}")
    print("-" * 50)

# Check specifically for Hindi voices
hindi_voices = [voice for voice in voices if "hindi" in voice.name.lower() or "hi-in" in voice.id.lower()]
if hindi_voices:
    print("\nHindi voices found:")
    for voice in hindi_voices:
        print(f"  ID: {voice.id}")
        print(f"  Name: {voice.name}")
else:
    print("\nNo Hindi voices found in the system.")

# Keep the window open
input("\nPress Enter to exit...")
