"""
Voice Assistant - Setup Script
-----------------------------
This script helps with setting up the Voice Assistant project.
It installs required dependencies and performs initial configuration.
"""

import subprocess
import os
import json
import sys

def check_python_version():
    """Check if Python version is compatible"""
    required_version = (3, 6)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current version: {current_version[0]}.{current_version[1]}")
        return False
    return True

def install_dependencies():
    """Install required packages from requirements.txt"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_default_config():
    """Create default configuration file if it doesn't exist"""
    if not os.path.exists('config.json'):
        print("Creating default configuration file...")
        default_config = {
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
            'voice': 0,
            'wake_word': 'assistant'
        }
        
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=4)
        print("Default configuration file created!")
    else:
        print("Configuration file already exists.")

def main():
    """Main setup function"""
    print("=" * 50)
    print("Voice Assistant Setup")
    print("=" * 50)
    
    if not check_python_version():
        return
    
    if install_dependencies():
        create_default_config()
        print("\nSetup completed successfully!")
        print("You can now run the voice assistant using:")
        print("  - python main.py")
        print("  - or double-click on run_assistant.bat")
    else:
        print("\nSetup failed. Please check the errors above and try again.")

if __name__ == "__main__":
    main()
