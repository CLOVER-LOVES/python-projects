"""
Background Voice Assistant Service
--------------------------------
This script runs the voice assistant in the background with minimal resource usage.
"""

import os
import sys
import time
import logging
import threading
import psutil
import signal
import argparse
from typing import Optional
import pystray
from PIL import Image, ImageDraw
import advanced_assistant

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("background_assistant.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BackgroundAssistant:
    """
    Run the voice assistant in the background with minimal resource usage
    """
    def __init__(self):
        """Initialize the background assistant"""
        self.assistant = None
        self.assistant_thread = None
        self.is_running = False
        self.tray_icon = None
        self.resource_monitor_thread = None

        # Resource usage limits
        self.max_cpu_percent = 30.0  # Maximum CPU usage percentage (increased from 15%)
        self.max_memory_mb = 300.0   # Maximum memory usage in MB (increased from 200MB)

        # Initialize the assistant
        self.initialize_assistant()

        # Create system tray icon
        self.create_tray_icon()

    def initialize_assistant(self) -> None:
        """Initialize the voice assistant"""
        try:
            # Create the advanced assistant
            self.assistant = advanced_assistant.AdvancedVoiceAssistant()
            logger.info("Voice assistant initialized")
        except Exception as e:
            logger.error(f"Error initializing voice assistant: {e}")
            sys.exit(1)

    def create_tray_icon(self) -> None:
        """Create a system tray icon"""
        try:
            # Create an icon image
            icon_size = 64
            icon_image = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(icon_image)

            # Draw a simple microphone icon
            draw.ellipse((16, 16, 48, 48), fill=(0, 120, 212))
            draw.rectangle((28, 24, 36, 40), fill=(255, 255, 255))
            draw.rectangle((28, 36, 36, 52), fill=(255, 255, 255))
            draw.ellipse((24, 48, 40, 56), fill=(255, 255, 255))

            # Create the tray icon
            self.tray_icon = pystray.Icon(
                "voice_assistant",
                icon_image,
                "Hey Clover Voice Assistant",
                menu=pystray.Menu(
                    pystray.MenuItem("Status", self.show_status, enabled=False),
                    pystray.MenuItem("Running", lambda: True, enabled=False),
                    pystray.Menu.SEPARATOR,
                    pystray.MenuItem("Start", self.start_assistant, enabled=lambda item: not self.is_running),
                    pystray.MenuItem("Stop", self.stop_assistant, enabled=lambda item: self.is_running),
                    pystray.Menu.SEPARATOR,
                    pystray.MenuItem("Exit", self.exit_application)
                )
            )

            logger.info("System tray icon created")
        except Exception as e:
            logger.error(f"Error creating system tray icon: {e}")
            # Continue without tray icon
            self.tray_icon = None

    def show_status(self) -> None:
        """Show the current status"""
        # This is just a placeholder for the status menu item
        pass

    def start_assistant(self) -> None:
        """Start the voice assistant in a separate thread"""
        if self.is_running:
            logger.warning("Assistant is already running")
            return

        try:
            # Create a new thread for the assistant
            self.assistant_thread = threading.Thread(target=self._assistant_thread_func)
            self.assistant_thread.daemon = True
            self.is_running = True
            self.assistant_thread.start()

            # Start resource monitoring
            self.start_resource_monitoring()

            logger.info("Voice assistant started")

            # Update tray icon tooltip
            if self.tray_icon:
                self.tray_icon.title = "Hey Clover Voice Assistant (Running)"
        except Exception as e:
            logger.error(f"Error starting voice assistant: {e}")
            self.is_running = False

    def _assistant_thread_func(self) -> None:
        """Thread function for running the assistant"""
        try:
            # Run the assistant
            self.assistant.run()
        except Exception as e:
            logger.error(f"Error in assistant thread: {e}")
        finally:
            self.is_running = False

            # Update tray icon tooltip
            if self.tray_icon:
                self.tray_icon.title = "Hey Clover Voice Assistant (Stopped)"

    def stop_assistant(self) -> None:
        """Stop the voice assistant"""
        if not self.is_running:
            logger.warning("Assistant is not running")
            return

        try:
            # Set the flag to stop the assistant
            self.is_running = False

            # Stop resource monitoring
            self.stop_resource_monitoring()

            # Wait for the thread to finish
            if self.assistant_thread and self.assistant_thread.is_alive():
                self.assistant_thread.join(timeout=2.0)

            logger.info("Voice assistant stopped")

            # Update tray icon tooltip
            if self.tray_icon:
                self.tray_icon.title = "Hey Clover Voice Assistant (Stopped)"
        except Exception as e:
            logger.error(f"Error stopping voice assistant: {e}")

    def start_resource_monitoring(self) -> None:
        """Start monitoring resource usage"""
        if self.resource_monitor_thread and self.resource_monitor_thread.is_alive():
            return

        self.resource_monitor_thread = threading.Thread(target=self._resource_monitor_thread_func)
        self.resource_monitor_thread.daemon = True
        self.resource_monitor_thread.start()

        logger.info("Resource monitoring started")

    def stop_resource_monitoring(self) -> None:
        """Stop monitoring resource usage"""
        # The thread will stop automatically when the assistant stops
        logger.info("Resource monitoring stopped")

    def _resource_monitor_thread_func(self) -> None:
        """Thread function for monitoring resource usage"""
        process = psutil.Process(os.getpid())

        while self.is_running:
            try:
                # Get CPU and memory usage
                cpu_percent = process.cpu_percent(interval=1.0)
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / (1024 * 1024)  # Convert to MB

                # Log resource usage every 60 seconds
                if int(time.time()) % 60 == 0:
                    logger.info(f"Resource usage: CPU: {cpu_percent:.1f}%, Memory: {memory_mb:.1f} MB")

                # Check if resource usage exceeds limits
                if cpu_percent > self.max_cpu_percent:
                    logger.warning(f"CPU usage too high: {cpu_percent:.1f}% (limit: {self.max_cpu_percent:.1f}%)")
                    # Implement CPU throttling here if needed

                if memory_mb > self.max_memory_mb:
                    logger.warning(f"Memory usage too high: {memory_mb:.1f} MB (limit: {self.max_memory_mb:.1f} MB)")
                    # Implement memory optimization here if needed

                # Sleep for a short time
                time.sleep(5.0)
            except Exception as e:
                logger.error(f"Error monitoring resources: {e}")
                time.sleep(10.0)

    def exit_application(self) -> None:
        """Exit the application"""
        logger.info("Exiting application")

        # Stop the assistant if it's running
        if self.is_running:
            self.stop_assistant()

        # Stop the tray icon
        if self.tray_icon:
            self.tray_icon.stop()

        # Exit the application
        sys.exit(0)

    def run(self) -> None:
        """Run the background assistant"""
        # Start the assistant
        self.start_assistant()

        # Run the tray icon
        if self.tray_icon:
            self.tray_icon.run()
        else:
            # If no tray icon, just keep the main thread alive
            try:
                while True:
                    time.sleep(1.0)
            except KeyboardInterrupt:
                self.exit_application()

def main():
    """Main function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the voice assistant in the background")
    parser.add_argument("--start", action="store_true", help="Start the assistant immediately")
    parser.add_argument("--no-tray", action="store_true", help="Run without system tray icon")
    args = parser.parse_args()

    # Create the background assistant
    assistant = BackgroundAssistant()

    # Start the assistant if requested
    if args.start:
        assistant.start_assistant()

    # Run the assistant
    assistant.run()

if __name__ == "__main__":
    main()
