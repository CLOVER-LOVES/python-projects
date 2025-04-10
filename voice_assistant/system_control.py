"""
System Control Module
-------------------
This module provides functions to control various aspects of the Windows operating system.
"""

import os
import sys
import subprocess
import ctypes
import time
import logging
import psutil
import platform
import pyautogui
import winreg
import win32api
import win32con
import win32gui
import win32process
import pywintypes
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemControl:
    """
    Class for controlling various system functions on Windows
    """
    def __init__(self):
        """Initialize the system control module"""
        self.system_info = self._get_system_info()
        logger.info("System Control module initialized")
    
    def _get_system_info(self) -> Dict:
        """Get basic system information"""
        try:
            info = {
                "os": platform.system(),
                "os_version": platform.version(),
                "os_release": platform.release(),
                "computer_name": platform.node(),
                "processor": platform.processor(),
                "architecture": platform.architecture()[0],
                "python_version": platform.python_version(),
            }
            return info
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {}
    
    # Volume Control Functions
    def set_volume(self, level: int) -> bool:
        """
        Set the system volume level (0-100)
        
        Args:
            level: Volume level from 0 (mute) to 100 (max)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure level is within valid range
            level = max(0, min(100, level))
            
            # Use PowerShell to set volume
            command = f'powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]174)" '
            for _ in range(50):  # First mute by sending volume down many times
                subprocess.run(command, shell=True, check=True)
            
            if level > 0:
                # Then raise to desired level
                up_command = f'powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]175)" '
                for _ in range(int(level / 2)):  # Each press is about 2%
                    subprocess.run(up_command, shell=True, check=True)
            
            logger.info(f"Volume set to {level}%")
            return True
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
            return False
    
    def volume_up(self, steps: int = 5) -> bool:
        """
        Increase system volume
        
        Args:
            steps: Number of steps to increase (each step is about 2%)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            command = f'powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]175)" '
            for _ in range(steps):
                subprocess.run(command, shell=True, check=True)
            logger.info(f"Volume increased by {steps} steps")
            return True
        except Exception as e:
            logger.error(f"Error increasing volume: {e}")
            return False
    
    def volume_down(self, steps: int = 5) -> bool:
        """
        Decrease system volume
        
        Args:
            steps: Number of steps to decrease (each step is about 2%)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            command = f'powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]174)" '
            for _ in range(steps):
                subprocess.run(command, shell=True, check=True)
            logger.info(f"Volume decreased by {steps} steps")
            return True
        except Exception as e:
            logger.error(f"Error decreasing volume: {e}")
            return False
    
    def mute_volume(self) -> bool:
        """
        Mute/unmute system volume
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            command = f'powershell -c "(New-Object -ComObject WScript.Shell).SendKeys([char]173)" '
            subprocess.run(command, shell=True, check=True)
            logger.info("Volume muted/unmuted")
            return True
        except Exception as e:
            logger.error(f"Error muting volume: {e}")
            return False
    
    # Screen Brightness Functions
    def set_brightness(self, level: int) -> bool:
        """
        Set screen brightness level (0-100)
        
        Args:
            level: Brightness level from 0 (min) to 100 (max)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure level is within valid range
            level = max(0, min(100, level))
            
            # Use PowerShell to set brightness
            command = f'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {level})"'
            subprocess.run(command, shell=True, check=True)
            
            logger.info(f"Brightness set to {level}%")
            return True
        except Exception as e:
            logger.error(f"Error setting brightness: {e}")
            return False
    
    # Power Management Functions
    def shutdown_computer(self, delay: int = 0) -> bool:
        """
        Shutdown the computer
        
        Args:
            delay: Delay in seconds before shutdown
            
        Returns:
            bool: True if command was sent successfully
        """
        try:
            os.system(f"shutdown /s /t {delay}")
            logger.info(f"Computer will shutdown in {delay} seconds")
            return True
        except Exception as e:
            logger.error(f"Error shutting down computer: {e}")
            return False
    
    def restart_computer(self, delay: int = 0) -> bool:
        """
        Restart the computer
        
        Args:
            delay: Delay in seconds before restart
            
        Returns:
            bool: True if command was sent successfully
        """
        try:
            os.system(f"shutdown /r /t {delay}")
            logger.info(f"Computer will restart in {delay} seconds")
            return True
        except Exception as e:
            logger.error(f"Error restarting computer: {e}")
            return False
    
    def sleep_computer(self) -> bool:
        """
        Put the computer to sleep
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            logger.info("Computer going to sleep")
            return True
        except Exception as e:
            logger.error(f"Error putting computer to sleep: {e}")
            return False
    
    def cancel_shutdown(self) -> bool:
        """
        Cancel a scheduled shutdown or restart
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            os.system("shutdown /a")
            logger.info("Scheduled shutdown/restart cancelled")
            return True
        except Exception as e:
            logger.error(f"Error cancelling shutdown: {e}")
            return False
    
    def lock_computer(self) -> bool:
        """
        Lock the computer
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            ctypes.windll.user32.LockWorkStation()
            logger.info("Computer locked")
            return True
        except Exception as e:
            logger.error(f"Error locking computer: {e}")
            return False
    
    # Screenshot Functions
    def take_screenshot(self, filename: Optional[str] = None) -> Optional[str]:
        """
        Take a screenshot and save it to a file
        
        Args:
            filename: Optional filename to save the screenshot
            
        Returns:
            str: Path to the saved screenshot or None if failed
        """
        try:
            if not filename:
                # Generate a filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            # Ensure the filename has .png extension
            if not filename.lower().endswith(".png"):
                filename += ".png"
            
            # Take the screenshot
            screenshot = pyautogui.screenshot()
            
            # Save the screenshot
            screenshot.save(filename)
            
            logger.info(f"Screenshot saved to {filename}")
            return os.path.abspath(filename)
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None
    
    # Application Management Functions
    def launch_application(self, app_name: str) -> bool:
        """
        Launch an application by name
        
        Args:
            app_name: Name of the application to launch
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Common applications dictionary (name -> executable path or command)
            common_apps = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
                "word": "winword.exe",
                "excel": "excel.exe",
                "powerpoint": "powerpnt.exe",
                "chrome": "chrome.exe",
                "edge": "msedge.exe",
                "firefox": "firefox.exe",
                "explorer": "explorer.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "control panel": "control.exe",
                "task manager": "taskmgr.exe",
                "settings": "ms-settings:",
                "photos": "ms-photos:",
                "camera": "microsoft.windows.camera:",
                "mail": "outlookmail:",
                "calendar": "outlookcal:",
                "maps": "bingmaps:",
                "store": "ms-windows-store:",
                "spotify": "spotify.exe",
                "vlc": "vlc.exe",
                "visual studio code": "code.exe",
                "visual studio": "devenv.exe",
                "discord": "discord.exe",
                "slack": "slack.exe",
                "zoom": "zoom.exe",
                "teams": "teams.exe"
            }
            
            # Check if the app is in our common apps dictionary
            app_name_lower = app_name.lower()
            if app_name_lower in common_apps:
                app_path = common_apps[app_name_lower]
                
                # Check if it's a Windows URI scheme
                if app_path.startswith("ms-"):
                    os.system(f"start {app_path}")
                else:
                    # Try to launch the application
                    subprocess.Popen(app_path, shell=True)
                
                logger.info(f"Launched application: {app_name}")
                return True
            else:
                # Try to launch by name directly
                subprocess.Popen(app_name, shell=True)
                logger.info(f"Attempted to launch application: {app_name}")
                return True
        except Exception as e:
            logger.error(f"Error launching application {app_name}: {e}")
            return False
    
    def close_application(self, app_name: str) -> bool:
        """
        Close an application by name
        
        Args:
            app_name: Name of the application to close
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get all running processes
            for proc in psutil.process_iter(['pid', 'name']):
                # Check if the process name contains the app name (case insensitive)
                if app_name.lower() in proc.info['name'].lower():
                    # Terminate the process
                    process = psutil.Process(proc.info['pid'])
                    process.terminate()
                    logger.info(f"Closed application: {proc.info['name']}")
                    return True
            
            logger.warning(f"Application not found: {app_name}")
            return False
        except Exception as e:
            logger.error(f"Error closing application {app_name}: {e}")
            return False
    
    # System Information Functions
    def get_battery_status(self) -> Dict:
        """
        Get battery status information
        
        Returns:
            dict: Battery status information
        """
        try:
            battery = psutil.sensors_battery()
            if battery:
                status = {
                    "percent": battery.percent,
                    "power_plugged": battery.power_plugged,
                    "time_left": battery.secsleft if battery.secsleft != -1 else None
                }
                
                # Convert seconds to hours and minutes
                if status["time_left"]:
                    hours, remainder = divmod(status["time_left"], 3600)
                    minutes, _ = divmod(remainder, 60)
                    status["time_left_formatted"] = f"{hours}h {minutes}m"
                
                return status
            else:
                return {"error": "No battery found"}
        except Exception as e:
            logger.error(f"Error getting battery status: {e}")
            return {"error": str(e)}
    
    def get_system_usage(self) -> Dict:
        """
        Get CPU, memory, and disk usage information
        
        Returns:
            dict: System usage information
        """
        try:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Get memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used / (1024 * 1024 * 1024)  # Convert to GB
            memory_total = memory.total / (1024 * 1024 * 1024)  # Convert to GB
            
            # Get disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used = disk.used / (1024 * 1024 * 1024)  # Convert to GB
            disk_total = disk.total / (1024 * 1024 * 1024)  # Convert to GB
            
            return {
                "cpu": {
                    "percent": cpu_percent
                },
                "memory": {
                    "percent": memory_percent,
                    "used_gb": round(memory_used, 2),
                    "total_gb": round(memory_total, 2)
                },
                "disk": {
                    "percent": disk_percent,
                    "used_gb": round(disk_used, 2),
                    "total_gb": round(disk_total, 2)
                }
            }
        except Exception as e:
            logger.error(f"Error getting system usage: {e}")
            return {"error": str(e)}
    
    def get_network_status(self) -> Dict:
        """
        Get network status information
        
        Returns:
            dict: Network status information
        """
        try:
            # Get network information
            network_info = {}
            
            # Get network connections
            connections = psutil.net_connections()
            network_info["active_connections"] = len(connections)
            
            # Get network interfaces
            interfaces = psutil.net_if_addrs()
            network_info["interfaces"] = {}
            
            for interface, addresses in interfaces.items():
                network_info["interfaces"][interface] = []
                for address in addresses:
                    if address.family == 2:  # IPv4
                        network_info["interfaces"][interface].append({
                            "ip": address.address,
                            "netmask": address.netmask,
                            "broadcast": address.broadcast
                        })
            
            # Get network statistics
            stats = psutil.net_io_counters()
            network_info["bytes_sent"] = stats.bytes_sent
            network_info["bytes_received"] = stats.bytes_recv
            
            return network_info
        except Exception as e:
            logger.error(f"Error getting network status: {e}")
            return {"error": str(e)}
    
    # File Operations Functions
    def search_files(self, query: str, path: str = None) -> List[str]:
        """
        Search for files matching a query
        
        Args:
            query: Search query
            path: Path to search in (default: user's home directory)
            
        Returns:
            list: List of matching file paths
        """
        try:
            if not path:
                path = os.path.expanduser("~")
            
            results = []
            query = query.lower()
            
            # Walk through the directory tree
            for root, _, files in os.walk(path):
                for file in files:
                    if query in file.lower():
                        results.append(os.path.join(root, file))
                        
                        # Limit results to prevent excessive searching
                        if len(results) >= 20:
                            return results
            
            return results
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return []
    
    def open_file(self, file_path: str) -> bool:
        """
        Open a file with the default application
        
        Args:
            file_path: Path to the file to open
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            os.startfile(os.path.normpath(file_path))
            logger.info(f"Opened file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error opening file {file_path}: {e}")
            return False
    
    def create_folder(self, folder_path: str) -> bool:
        """
        Create a new folder
        
        Args:
            folder_path: Path to the folder to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"Created folder: {folder_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating folder {folder_path}: {e}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
                return True
            else:
                logger.warning(f"File not found: {file_path}")
                return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False
    
    # Clipboard Functions
    def get_clipboard_text(self) -> Optional[str]:
        """
        Get text from clipboard
        
        Returns:
            str: Clipboard text or None if failed
        """
        try:
            return pyautogui.hotkey('ctrl', 'c')
        except Exception as e:
            logger.error(f"Error getting clipboard text: {e}")
            return None
    
    def set_clipboard_text(self, text: str) -> bool:
        """
        Set text to clipboard
        
        Args:
            text: Text to set to clipboard
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            pyautogui.write(text)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'c')
            logger.info("Text copied to clipboard")
            return True
        except Exception as e:
            logger.error(f"Error setting clipboard text: {e}")
            return False
    
    # Keyboard and Mouse Functions
    def press_key(self, key: str) -> bool:
        """
        Press a keyboard key
        
        Args:
            key: Key to press
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            pyautogui.press(key)
            logger.info(f"Pressed key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error pressing key {key}: {e}")
            return False
    
    def type_text(self, text: str) -> bool:
        """
        Type text
        
        Args:
            text: Text to type
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            pyautogui.write(text)
            logger.info(f"Typed text: {text}")
            return True
        except Exception as e:
            logger.error(f"Error typing text: {e}")
            return False
    
    def click_mouse(self, x: int = None, y: int = None, button: str = "left") -> bool:
        """
        Click the mouse
        
        Args:
            x: X coordinate (default: current position)
            y: Y coordinate (default: current position)
            button: Mouse button to click ("left", "right", "middle")
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y, button=button)
            else:
                pyautogui.click(button=button)
            
            logger.info(f"Clicked {button} mouse button")
            return True
        except Exception as e:
            logger.error(f"Error clicking mouse: {e}")
            return False

# Example usage
if __name__ == "__main__":
    system = SystemControl()
    
    # Get system information
    print("System Information:")
    for key, value in system.system_info.items():
        print(f"  {key}: {value}")
    
    # Get battery status
    battery = system.get_battery_status()
    if "error" not in battery:
        print(f"\nBattery: {battery['percent']}% {'(Charging)' if battery['power_plugged'] else '(Discharging)'}")
        if battery.get("time_left_formatted"):
            print(f"Time left: {battery['time_left_formatted']}")
    
    # Get system usage
    usage = system.get_system_usage()
    if "error" not in usage:
        print(f"\nCPU Usage: {usage['cpu']['percent']}%")
        print(f"Memory Usage: {usage['memory']['percent']}% ({usage['memory']['used_gb']} GB / {usage['memory']['total_gb']} GB)")
        print(f"Disk Usage: {usage['disk']['percent']}% ({usage['disk']['used_gb']} GB / {usage['disk']['total_gb']} GB)")
