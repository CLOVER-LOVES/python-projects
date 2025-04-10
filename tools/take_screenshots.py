import os
import time
import argparse
from PIL import ImageGrab
from datetime import datetime

def take_screenshot(output_dir, name=None, delay=0):
    """
    Take a screenshot and save it to the specified directory.
    
    Args:
        output_dir (str): Directory to save the screenshot
        name (str, optional): Name for the screenshot file. If None, uses timestamp.
        delay (int, optional): Delay in seconds before taking the screenshot.
    
    Returns:
        str: Path to the saved screenshot
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Wait for the specified delay
    if delay > 0:
        print(f"Taking screenshot in {delay} seconds...")
        time.sleep(delay)
    
    # Take the screenshot
    screenshot = ImageGrab.grab()
    
    # Generate filename
    if name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
    else:
        filename = f"{name}.png"
    
    # Save the screenshot
    filepath = os.path.join(output_dir, filename)
    screenshot.save(filepath)
    print(f"Screenshot saved to: {filepath}")
    
    return filepath

def main():
    parser = argparse.ArgumentParser(description="Take screenshots for documentation")
    parser.add_argument("--output", "-o", default="docs/assets/images", 
                        help="Directory to save screenshots")
    parser.add_argument("--name", "-n", help="Name for the screenshot file")
    parser.add_argument("--delay", "-d", type=int, default=5,
                        help="Delay in seconds before taking the screenshot")
    
    args = parser.parse_args()
    
    print("Position your application window and get ready...")
    take_screenshot(args.output, args.name, args.delay)

if __name__ == "__main__":
    main()
