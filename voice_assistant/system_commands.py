"""
System Commands Module
-------------------
This module provides command classes for system control functions.
"""

import os
import re
import logging
from typing import List, Dict, Optional, Any
from enhanced_voice_assistant import Command
from system_control import SystemControl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VolumeCommand(Command):
    """Control system volume"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.system = SystemControl()
    
    def matches(self, query: str) -> bool:
        return ('volume' in query or 
                'louder' in query or 
                'quieter' in query or 
                'mute' in query or 
                'unmute' in query)
    
    def execute(self, query: str) -> bool:
        query = query.lower()
        
        # Check for volume up
        if 'up' in query or 'increase' in query or 'louder' in query or 'raise' in query:
            # Check if a specific amount is mentioned
            steps = 5  # Default steps
            match = re.search(r'(\d+)', query)
            if match:
                steps = int(match.group(1))
                steps = min(20, max(1, steps))  # Limit between 1 and 20
            
            if self.system.volume_up(steps):
                self.assistant.speak(f"Volume increased")
                return True
            else:
                self.assistant.speak("I couldn't change the volume")
                return False
        
        # Check for volume down
        elif 'down' in query or 'decrease' in query or 'quieter' in query or 'lower' in query:
            # Check if a specific amount is mentioned
            steps = 5  # Default steps
            match = re.search(r'(\d+)', query)
            if match:
                steps = int(match.group(1))
                steps = min(20, max(1, steps))  # Limit between 1 and 20
            
            if self.system.volume_down(steps):
                self.assistant.speak(f"Volume decreased")
                return True
            else:
                self.assistant.speak("I couldn't change the volume")
                return False
        
        # Check for mute/unmute
        elif 'mute' in query or 'unmute' in query:
            if self.system.mute_volume():
                self.assistant.speak("Volume toggled")
                return True
            else:
                self.assistant.speak("I couldn't change the volume")
                return False
        
        # Check for set volume to specific level
        elif 'set' in query or 'to' in query:
            # Try to extract a number
            match = re.search(r'(\d+)', query)
            if match:
                level = int(match.group(1))
                level = min(100, max(0, level))  # Ensure between 0 and 100
                
                if self.system.set_volume(level):
                    self.assistant.speak(f"Volume set to {level} percent")
                    return True
                else:
                    self.assistant.speak("I couldn't set the volume")
                    return False
        
        # If we get here, we didn't understand the command
        self.assistant.speak("I'm not sure how to change the volume like that")
        return False

class BrightnessCommand(Command):
    """Control screen brightness"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.system = SystemControl()
    
    def matches(self, query: str) -> bool:
        return 'brightness' in query or 'screen' in query
    
    def execute(self, query: str) -> bool:
        query = query.lower()
        
        # Check for set brightness to specific level
        if ('set' in query or 'to' in query) and ('brightness' in query or 'screen' in query):
            # Try to extract a number
            match = re.search(r'(\d+)', query)
            if match:
                level = int(match.group(1))
                level = min(100, max(0, level))  # Ensure between 0 and 100
                
                if self.system.set_brightness(level):
                    self.assistant.speak(f"Brightness set to {level} percent")
                    return True
                else:
                    self.assistant.speak("I couldn't set the brightness")
                    return False
            else:
                self.assistant.speak("Please specify a brightness level between 0 and 100")
                return False
        
        # If we get here, we didn't understand the command
        self.assistant.speak("I'm not sure how to change the brightness like that")
        return False

class PowerCommand(Command):
    """Control power functions (shutdown, restart, sleep)"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.system = SystemControl()
    
    def matches(self, query: str) -> bool:
        return ('shutdown' in query or 
                'restart' in query or 
                'reboot' in query or 
                'sleep' in query or 
                'lock' in query or 
                'log off' in query or 
                'sign out' in query or
                'turn off computer' in query)
    
    def execute(self, query: str) -> bool:
        query = query.lower()
        
        # Check for shutdown
        if 'shutdown' in query or 'turn off computer' in query:
            # Check if a delay is specified
            delay = 0
            match = re.search(r'(\d+)\s*(second|minute)', query)
            if match:
                amount = int(match.group(1))
                unit = match.group(2)
                
                if unit.startswith('minute'):
                    delay = amount * 60
                else:
                    delay = amount
            
            # Confirm with the user
            self.assistant.speak(f"Are you sure you want to shutdown the computer{' in ' + str(delay) + ' seconds' if delay > 0 else ''}?")
            confirmation = self.assistant.take_command()
            
            if confirmation and ('yes' in confirmation.lower() or 'sure' in confirmation.lower()):
                if self.system.shutdown_computer(delay):
                    self.assistant.speak(f"Shutting down the computer{' in ' + str(delay) + ' seconds' if delay > 0 else ''}")
                    return True
                else:
                    self.assistant.speak("I couldn't shutdown the computer")
                    return False
            else:
                self.assistant.speak("Shutdown cancelled")
                return True
        
        # Check for restart
        elif 'restart' in query or 'reboot' in query:
            # Check if a delay is specified
            delay = 0
            match = re.search(r'(\d+)\s*(second|minute)', query)
            if match:
                amount = int(match.group(1))
                unit = match.group(2)
                
                if unit.startswith('minute'):
                    delay = amount * 60
                else:
                    delay = amount
            
            # Confirm with the user
            self.assistant.speak(f"Are you sure you want to restart the computer{' in ' + str(delay) + ' seconds' if delay > 0 else ''}?")
            confirmation = self.assistant.take_command()
            
            if confirmation and ('yes' in confirmation.lower() or 'sure' in confirmation.lower()):
                if self.system.restart_computer(delay):
                    self.assistant.speak(f"Restarting the computer{' in ' + str(delay) + ' seconds' if delay > 0 else ''}")
                    return True
                else:
                    self.assistant.speak("I couldn't restart the computer")
                    return False
            else:
                self.assistant.speak("Restart cancelled")
                return True
        
        # Check for sleep
        elif 'sleep' in query:
            if self.system.sleep_computer():
                self.assistant.speak("Putting the computer to sleep")
                return True
            else:
                self.assistant.speak("I couldn't put the computer to sleep")
                return False
        
        # Check for lock
        elif 'lock' in query:
            if self.system.lock_computer():
                self.assistant.speak("Locking the computer")
                return True
            else:
                self.assistant.speak("I couldn't lock the computer")
                return False
        
        # Check for cancel shutdown/restart
        elif 'cancel' in query and ('shutdown' in query or 'restart' in query):
            if self.system.cancel_shutdown():
                self.assistant.speak("Cancelled the scheduled shutdown or restart")
                return True
            else:
                self.assistant.speak("I couldn't cancel the shutdown or restart")
                return False
        
        # If we get here, we didn't understand the command
        self.assistant.speak("I'm not sure how to do that power operation")
        return False

class ScreenshotCommand(Command):
    """Take screenshots"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.system = SystemControl()
    
    def matches(self, query: str) -> bool:
        return 'screenshot' in query or 'capture screen' in query or 'screen capture' in query
    
    def execute(self, query: str) -> bool:
        # Take a screenshot
        screenshot_path = self.system.take_screenshot()
        
        if screenshot_path:
            self.assistant.speak(f"Screenshot taken and saved to {screenshot_path}")
            return True
        else:
            self.assistant.speak("I couldn't take a screenshot")
            return False

class ApplicationCommand(Command):
    """Launch and close applications"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.system = SystemControl()
    
    def matches(self, query: str) -> bool:
        return (('open' in query or 'launch' in query or 'start' in query or 'run' in query) or
                ('close' in query or 'exit' in query or 'quit' in query))
    
    def execute(self, query: str) -> bool:
        query = query.lower()
        
        # Check for open/launch application
        if 'open' in query or 'launch' in query or 'start' in query or 'run' in query:
            # Try to extract the application name
            app_name = None
            
            if 'open' in query:
                app_name = query.split('open', 1)[1].strip()
            elif 'launch' in query:
                app_name = query.split('launch', 1)[1].strip()
            elif 'start' in query:
                app_name = query.split('start', 1)[1].strip()
            elif 'run' in query:
                app_name = query.split('run', 1)[1].strip()
            
            if app_name:
                if self.system.launch_application(app_name):
                    self.assistant.speak(f"Opening {app_name}")
                    return True
                else:
                    self.assistant.speak(f"I couldn't open {app_name}")
                    return False
            else:
                self.assistant.speak("Please specify an application to open")
                return False
        
        # Check for close application
        elif 'close' in query or 'exit' in query or 'quit' in query:
            # Try to extract the application name
            app_name = None
            
            if 'close' in query:
                app_name = query.split('close', 1)[1].strip()
            elif 'exit' in query:
                app_name = query.split('exit', 1)[1].strip()
            elif 'quit' in query:
                app_name = query.split('quit', 1)[1].strip()
            
            if app_name:
                if self.system.close_application(app_name):
                    self.assistant.speak(f"Closed {app_name}")
                    return True
                else:
                    self.assistant.speak(f"I couldn't close {app_name}")
                    return False
            else:
                self.assistant.speak("Please specify an application to close")
                return False
        
        # If we get here, we didn't understand the command
        self.assistant.speak("I'm not sure which application you want to manage")
        return False

class SystemInfoCommand(Command):
    """Get system information"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.system = SystemControl()
    
    def matches(self, query: str) -> bool:
        return (('battery' in query or 'power' in query) or
                ('cpu' in query or 'processor' in query or 'memory' in query or 'ram' in query) or
                ('disk' in query or 'storage' in query or 'drive' in query) or
                ('network' in query or 'internet' in query or 'wifi' in query) or
                ('system' in query and 'info' in query))
    
    def execute(self, query: str) -> bool:
        query = query.lower()
        
        # Check for battery status
        if 'battery' in query or 'power' in query:
            battery = self.system.get_battery_status()
            
            if "error" not in battery:
                status = "charging" if battery['power_plugged'] else "discharging"
                message = f"Battery is at {battery['percent']} percent and {status}"
                
                if battery.get("time_left_formatted") and not battery['power_plugged']:
                    message += f". Estimated time remaining: {battery['time_left_formatted']}"
                
                self.assistant.speak(message)
                return True
            else:
                self.assistant.speak("I couldn't get battery information")
                return False
        
        # Check for CPU/memory usage
        elif 'cpu' in query or 'processor' in query or 'memory' in query or 'ram' in query:
            usage = self.system.get_system_usage()
            
            if "error" not in usage:
                if 'cpu' in query or 'processor' in query:
                    self.assistant.speak(f"CPU usage is at {usage['cpu']['percent']} percent")
                elif 'memory' in query or 'ram' in query:
                    self.assistant.speak(f"Memory usage is at {usage['memory']['percent']} percent. {usage['memory']['used_gb']} gigabytes used out of {usage['memory']['total_gb']} gigabytes total")
                return True
            else:
                self.assistant.speak("I couldn't get system usage information")
                return False
        
        # Check for disk/storage usage
        elif 'disk' in query or 'storage' in query or 'drive' in query:
            usage = self.system.get_system_usage()
            
            if "error" not in usage:
                self.assistant.speak(f"Disk usage is at {usage['disk']['percent']} percent. {usage['disk']['used_gb']} gigabytes used out of {usage['disk']['total_gb']} gigabytes total")
                return True
            else:
                self.assistant.speak("I couldn't get disk usage information")
                return False
        
        # Check for network status
        elif 'network' in query or 'internet' in query or 'wifi' in query:
            network = self.system.get_network_status()
            
            if "error" not in network:
                # Count active interfaces
                active_interfaces = 0
                for interface, addresses in network["interfaces"].items():
                    if addresses:
                        active_interfaces += 1
                
                self.assistant.speak(f"You have {active_interfaces} active network interfaces and {network['active_connections']} active network connections")
                return True
            else:
                self.assistant.speak("I couldn't get network information")
                return False
        
        # Check for general system info
        elif 'system' in query and 'info' in query:
            info = self.system.system_info
            
            if info:
                self.assistant.speak(f"You are running {info['os']} {info['os_release']} on a {info['architecture']} system")
                return True
            else:
                self.assistant.speak("I couldn't get system information")
                return False
        
        # If we get here, we didn't understand the command
        self.assistant.speak("I'm not sure what system information you want")
        return False

class FileCommand(Command):
    """File operations"""
    def __init__(self, assistant):
        super().__init__(assistant)
        self.system = SystemControl()
    
    def matches(self, query: str) -> bool:
        return (('find' in query or 'search' in query or 'locate' in query) and ('file' in query or 'document' in query)) or \
               (('open' in query or 'create' in query or 'delete' in query) and ('file' in query or 'folder' in query or 'directory' in query))
    
    def execute(self, query: str) -> bool:
        query = query.lower()
        
        # Check for file search
        if ('find' in query or 'search' in query or 'locate' in query) and ('file' in query or 'document' in query):
            # Try to extract the search term
            search_term = None
            
            if 'find' in query and 'file' in query:
                parts = query.split('find', 1)[1].split('file', 1)
                if len(parts) > 1:
                    search_term = parts[1].strip()
                else:
                    search_term = parts[0].strip()
            elif 'search' in query and 'file' in query:
                parts = query.split('search', 1)[1].split('file', 1)
                if len(parts) > 1:
                    search_term = parts[1].strip()
                else:
                    search_term = parts[0].strip()
            elif 'locate' in query and 'file' in query:
                parts = query.split('locate', 1)[1].split('file', 1)
                if len(parts) > 1:
                    search_term = parts[1].strip()
                else:
                    search_term = parts[0].strip()
            
            # Clean up the search term
            if search_term:
                # Remove common words and prepositions
                for word in ['for', 'named', 'called', 'with', 'containing', 'that', 'has', 'the', 'a', 'an']:
                    search_term = search_term.replace(f" {word} ", " ")
                
                search_term = search_term.strip()
            
            if search_term:
                self.assistant.speak(f"Searching for files with '{search_term}' in the name")
                results = self.system.search_files(search_term)
                
                if results:
                    if len(results) == 1:
                        self.assistant.speak(f"I found 1 file: {os.path.basename(results[0])}")
                        self.assistant.speak("Would you like me to open it?")
                        response = self.assistant.take_command()
                        
                        if response and ('yes' in response.lower() or 'sure' in response.lower() or 'open' in response.lower()):
                            if self.system.open_file(results[0]):
                                self.assistant.speak(f"Opening {os.path.basename(results[0])}")
                                return True
                            else:
                                self.assistant.speak(f"I couldn't open the file")
                                return False
                    else:
                        self.assistant.speak(f"I found {len(results)} files. Here are the first few:")
                        for i, result in enumerate(results[:5]):
                            self.assistant.speak(f"{i+1}. {os.path.basename(result)}")
                        
                        self.assistant.speak("Would you like me to open one of these files?")
                        response = self.assistant.take_command()
                        
                        if response and ('yes' in response.lower() or 'sure' in response.lower() or 'open' in response.lower()):
                            # Try to extract a number
                            match = re.search(r'(\d+)', response)
                            if match:
                                index = int(match.group(1)) - 1
                                if 0 <= index < len(results):
                                    if self.system.open_file(results[index]):
                                        self.assistant.speak(f"Opening {os.path.basename(results[index])}")
                                        return True
                                    else:
                                        self.assistant.speak(f"I couldn't open the file")
                                        return False
                                else:
                                    self.assistant.speak("That's not a valid file number")
                                    return False
                            else:
                                self.assistant.speak("Please specify which file number to open")
                                return False
                    
                    return True
                else:
                    self.assistant.speak(f"I couldn't find any files matching '{search_term}'")
                    return False
            else:
                self.assistant.speak("Please specify what file you're looking for")
                return False
        
        # Check for create folder
        elif 'create' in query and ('folder' in query or 'directory' in query):
            # Try to extract the folder name
            folder_name = None
            
            if 'folder' in query:
                parts = query.split('folder', 1)
                if len(parts) > 1:
                    folder_name = parts[1].strip()
                else:
                    folder_name = parts[0].strip()
            elif 'directory' in query:
                parts = query.split('directory', 1)
                if len(parts) > 1:
                    folder_name = parts[1].strip()
                else:
                    folder_name = parts[0].strip()
            
            # Clean up the folder name
            if folder_name:
                # Remove common words and prepositions
                for word in ['named', 'called', 'with', 'the', 'a', 'an']:
                    folder_name = folder_name.replace(f" {word} ", " ")
                
                folder_name = folder_name.strip()
            
            if folder_name:
                # Create the folder in the user's home directory
                folder_path = os.path.join(os.path.expanduser("~"), folder_name)
                
                if self.system.create_folder(folder_path):
                    self.assistant.speak(f"Created folder '{folder_name}' in your home directory")
                    return True
                else:
                    self.assistant.speak(f"I couldn't create the folder")
                    return False
            else:
                self.assistant.speak("Please specify a name for the folder")
                return False
        
        # If we get here, we didn't understand the command
        self.assistant.speak("I'm not sure what file operation you want to perform")
        return False

# Function to get all system commands
def get_system_commands(assistant):
    """Get all system command classes"""
    return [
        VolumeCommand(assistant),
        BrightnessCommand(assistant),
        PowerCommand(assistant),
        ScreenshotCommand(assistant),
        ApplicationCommand(assistant),
        SystemInfoCommand(assistant),
        FileCommand(assistant)
    ]
