# Development Tools

This directory contains various tools to help with development and documentation.

## Screenshot Tool

The `take_screenshots.py` script allows you to take screenshots of your applications for documentation purposes.

### Usage

```bash
python tools/take_screenshots.py --name voice-assistant-demo --delay 5
```

### Options

- `--output`, `-o`: Directory to save screenshots (default: docs/assets/images)
- `--name`, `-n`: Name for the screenshot file (default: timestamp)
- `--delay`, `-d`: Delay in seconds before taking the screenshot (default: 5)

### Requirements

- Pillow (PIL): `pip install pillow`
