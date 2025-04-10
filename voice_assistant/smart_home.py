"""
Smart Home Control Module
-----------------------
This module provides integration with various smart home devices and platforms.
"""

import requests
import json
import logging
import time
import threading
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SmartHomeController:
    """
    Controller for smart home devices across different platforms
    """
    def __init__(self, config_file="smart_home_config.json"):
        """
        Initialize the smart home controller.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.config_file = config_file
        self.config = self.load_config()
        self.devices = {}
        self.platforms = {}
        
        # Initialize platforms based on configuration
        self.initialize_platforms()
    
    def load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_file} not found, creating default")
            default_config = {
                "platforms": {
                    "hue": {
                        "enabled": False,
                        "bridge_ip": "",
                        "username": ""
                    },
                    "tuya": {
                        "enabled": False,
                        "api_key": "",
                        "api_secret": "",
                        "region": "us"
                    },
                    "home_assistant": {
                        "enabled": False,
                        "url": "http://homeassistant.local:8123",
                        "token": ""
                    }
                },
                "device_aliases": {
                    "living room light": "hue:1",
                    "kitchen light": "hue:2",
                    "bedroom light": "tuya:device1",
                    "tv": "home_assistant:media_player.tv"
                }
            }
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def initialize_platforms(self):
        """Initialize enabled smart home platforms"""
        platforms_config = self.config.get("platforms", {})
        
        # Initialize Philips Hue
        if platforms_config.get("hue", {}).get("enabled", False):
            self.platforms["hue"] = HuePlatform(
                bridge_ip=platforms_config["hue"].get("bridge_ip", ""),
                username=platforms_config["hue"].get("username", "")
            )
        
        # Initialize Tuya
        if platforms_config.get("tuya", {}).get("enabled", False):
            self.platforms["tuya"] = TuyaPlatform(
                api_key=platforms_config["tuya"].get("api_key", ""),
                api_secret=platforms_config["tuya"].get("api_secret", ""),
                region=platforms_config["tuya"].get("region", "us")
            )
        
        # Initialize Home Assistant
        if platforms_config.get("home_assistant", {}).get("enabled", False):
            self.platforms["home_assistant"] = HomeAssistantPlatform(
                url=platforms_config["home_assistant"].get("url", ""),
                token=platforms_config["home_assistant"].get("token", "")
            )
        
        # Discover devices on all platforms
        self.discover_devices()
    
    def discover_devices(self):
        """Discover devices on all enabled platforms"""
        self.devices = {}
        
        for platform_name, platform in self.platforms.items():
            try:
                platform_devices = platform.discover_devices()
                
                for device_id, device_info in platform_devices.items():
                    full_id = f"{platform_name}:{device_id}"
                    self.devices[full_id] = {
                        "platform": platform_name,
                        "id": device_id,
                        "name": device_info.get("name", "Unknown"),
                        "type": device_info.get("type", "unknown"),
                        "state": device_info.get("state", {})
                    }
                
                logger.info(f"Discovered {len(platform_devices)} devices on {platform_name}")
            except Exception as e:
                logger.error(f"Error discovering devices on {platform_name}: {e}")
    
    def get_device_by_alias(self, alias: str) -> Optional[Dict]:
        """
        Get device by its alias.
        
        Args:
            alias (str): Device alias
            
        Returns:
            dict: Device information or None if not found
        """
        device_aliases = self.config.get("device_aliases", {})
        device_id = device_aliases.get(alias.lower())
        
        if not device_id:
            return None
        
        return self.devices.get(device_id)
    
    def control_device(self, device_identifier: str, command: str, params: Dict = None) -> bool:
        """
        Control a smart home device.
        
        Args:
            device_identifier (str): Device ID or alias
            command (str): Command to execute (e.g., "on", "off", "set_brightness")
            params (dict): Additional parameters for the command
            
        Returns:
            bool: True if successful, False otherwise
        """
        if params is None:
            params = {}
        
        # Check if the identifier is an alias
        device = self.get_device_by_alias(device_identifier)
        
        # If not an alias, check if it's a direct device ID
        if not device and device_identifier in self.devices:
            device = self.devices[device_identifier]
        
        if not device:
            logger.error(f"Device '{device_identifier}' not found")
            return False
        
        platform_name = device["platform"]
        device_id = device["id"]
        
        if platform_name not in self.platforms:
            logger.error(f"Platform '{platform_name}' not available")
            return False
        
        try:
            result = self.platforms[platform_name].control_device(device_id, command, params)
            
            if result:
                # Update device state
                self.devices[f"{platform_name}:{device_id}"]["state"] = result
            
            return bool(result)
        except Exception as e:
            logger.error(f"Error controlling device '{device_identifier}': {e}")
            return False
    
    def get_device_state(self, device_identifier: str) -> Optional[Dict]:
        """
        Get the current state of a device.
        
        Args:
            device_identifier (str): Device ID or alias
            
        Returns:
            dict: Device state or None if not found
        """
        # Check if the identifier is an alias
        device = self.get_device_by_alias(device_identifier)
        
        # If not an alias, check if it's a direct device ID
        if not device and device_identifier in self.devices:
            device = self.devices[device_identifier]
        
        if not device:
            logger.error(f"Device '{device_identifier}' not found")
            return None
        
        platform_name = device["platform"]
        device_id = device["id"]
        
        if platform_name not in self.platforms:
            logger.error(f"Platform '{platform_name}' not available")
            return None
        
        try:
            state = self.platforms[platform_name].get_device_state(device_id)
            
            if state:
                # Update device state
                self.devices[f"{platform_name}:{device_id}"]["state"] = state
            
            return state
        except Exception as e:
            logger.error(f"Error getting state for device '{device_identifier}': {e}")
            return None
    
    def add_device_alias(self, alias: str, device_id: str) -> bool:
        """
        Add an alias for a device.
        
        Args:
            alias (str): Alias for the device
            device_id (str): Full device ID (platform:id)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if device_id not in self.devices:
            logger.error(f"Device '{device_id}' not found")
            return False
        
        if "device_aliases" not in self.config:
            self.config["device_aliases"] = {}
        
        self.config["device_aliases"][alias.lower()] = device_id
        self.save_config()
        
        logger.info(f"Added alias '{alias}' for device '{device_id}'")
        return True
    
    def remove_device_alias(self, alias: str) -> bool:
        """
        Remove a device alias.
        
        Args:
            alias (str): Alias to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        if "device_aliases" not in self.config:
            return False
        
        if alias.lower() not in self.config["device_aliases"]:
            logger.error(f"Alias '{alias}' not found")
            return False
        
        del self.config["device_aliases"][alias.lower()]
        self.save_config()
        
        logger.info(f"Removed alias '{alias}'")
        return True
    
    def get_all_devices(self) -> Dict:
        """
        Get all discovered devices.
        
        Returns:
            dict: All devices
        """
        return self.devices
    
    def get_all_aliases(self) -> Dict:
        """
        Get all device aliases.
        
        Returns:
            dict: All aliases
        """
        return self.config.get("device_aliases", {})

class SmartHomePlatform:
    """Base class for smart home platforms"""
    def discover_devices(self) -> Dict:
        """
        Discover devices on the platform.
        
        Returns:
            dict: Discovered devices
        """
        raise NotImplementedError("Subclasses must implement discover_devices()")
    
    def control_device(self, device_id: str, command: str, params: Dict = None) -> Optional[Dict]:
        """
        Control a device.
        
        Args:
            device_id (str): Device ID
            command (str): Command to execute
            params (dict): Additional parameters
            
        Returns:
            dict: Updated device state or None if failed
        """
        raise NotImplementedError("Subclasses must implement control_device()")
    
    def get_device_state(self, device_id: str) -> Optional[Dict]:
        """
        Get device state.
        
        Args:
            device_id (str): Device ID
            
        Returns:
            dict: Device state or None if failed
        """
        raise NotImplementedError("Subclasses must implement get_device_state()")

class HuePlatform(SmartHomePlatform):
    """Philips Hue integration"""
    def __init__(self, bridge_ip: str, username: str):
        self.bridge_ip = bridge_ip
        self.username = username
        self.base_url = f"http://{bridge_ip}/api/{username}"
    
    def discover_devices(self) -> Dict:
        """Discover Hue devices"""
        devices = {}
        
        try:
            # Get all lights
            response = requests.get(f"{self.base_url}/lights")
            if response.status_code == 200:
                lights = response.json()
                
                for light_id, light_info in lights.items():
                    devices[light_id] = {
                        "name": light_info.get("name", f"Light {light_id}"),
                        "type": "light",
                        "state": light_info.get("state", {})
                    }
            
            # Get all groups
            response = requests.get(f"{self.base_url}/groups")
            if response.status_code == 200:
                groups = response.json()
                
                for group_id, group_info in groups.items():
                    devices[f"group_{group_id}"] = {
                        "name": group_info.get("name", f"Group {group_id}"),
                        "type": "group",
                        "state": group_info.get("state", {})
                    }
            
            return devices
        except Exception as e:
            logger.error(f"Error discovering Hue devices: {e}")
            return {}
    
    def control_device(self, device_id: str, command: str, params: Dict = None) -> Optional[Dict]:
        """Control a Hue device"""
        if params is None:
            params = {}
        
        try:
            # Check if it's a group
            is_group = device_id.startswith("group_")
            
            if is_group:
                group_id = device_id[6:]  # Remove "group_" prefix
                url = f"{self.base_url}/groups/{group_id}/action"
            else:
                url = f"{self.base_url}/lights/{device_id}/state"
            
            # Prepare the payload based on the command
            payload = {}
            
            if command == "on":
                payload["on"] = True
            elif command == "off":
                payload["on"] = False
            elif command == "set_brightness":
                brightness = params.get("brightness", 100)
                # Hue brightness is 0-254
                payload["bri"] = min(254, max(0, int(brightness * 2.54)))
            elif command == "set_color":
                # Convert RGB to Hue color space (simplified)
                if "rgb" in params:
                    r, g, b = params["rgb"]
                    # This is a simplified conversion
                    payload["xy"] = [
                        0.3 * r + 0.6 * g + 0.1 * b,
                        0.3 * r + 0.6 * g + 0.1 * b
                    ]
            
            # Send the command
            response = requests.put(url, json=payload)
            
            if response.status_code == 200:
                # Get updated state
                return self.get_device_state(device_id)
            else:
                logger.error(f"Error controlling Hue device: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error controlling Hue device: {e}")
            return None
    
    def get_device_state(self, device_id: str) -> Optional[Dict]:
        """Get Hue device state"""
        try:
            # Check if it's a group
            is_group = device_id.startswith("group_")
            
            if is_group:
                group_id = device_id[6:]  # Remove "group_" prefix
                url = f"{self.base_url}/groups/{group_id}"
            else:
                url = f"{self.base_url}/lights/{device_id}"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                device_info = response.json()
                
                if is_group:
                    return device_info.get("action", {})
                else:
                    return device_info.get("state", {})
            else:
                logger.error(f"Error getting Hue device state: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting Hue device state: {e}")
            return None

class TuyaPlatform(SmartHomePlatform):
    """Tuya Smart integration"""
    def __init__(self, api_key: str, api_secret: str, region: str = "us"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.region = region
        self.devices_cache = {}
        
        # Note: This is a simplified implementation
        # A real implementation would use the Tuya IoT Platform API
    
    def discover_devices(self) -> Dict:
        """
        Discover Tuya devices
        
        Note: This is a placeholder. A real implementation would use the Tuya API.
        """
        # In a real implementation, you would call the Tuya API to get devices
        # For now, we'll return an empty dict
        logger.warning("Tuya device discovery not fully implemented")
        return self.devices_cache
    
    def control_device(self, device_id: str, command: str, params: Dict = None) -> Optional[Dict]:
        """
        Control a Tuya device
        
        Note: This is a placeholder. A real implementation would use the Tuya API.
        """
        logger.warning("Tuya device control not fully implemented")
        return None
    
    def get_device_state(self, device_id: str) -> Optional[Dict]:
        """
        Get Tuya device state
        
        Note: This is a placeholder. A real implementation would use the Tuya API.
        """
        logger.warning("Tuya device state retrieval not fully implemented")
        return self.devices_cache.get(device_id, {}).get("state")

class HomeAssistantPlatform(SmartHomePlatform):
    """Home Assistant integration"""
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def discover_devices(self) -> Dict:
        """Discover Home Assistant devices"""
        devices = {}
        
        try:
            # Get all states
            response = requests.get(f"{self.url}/api/states", headers=self.headers)
            
            if response.status_code == 200:
                states = response.json()
                
                for entity in states:
                    entity_id = entity["entity_id"]
                    domain = entity_id.split(".")[0]
                    
                    # Only include certain types of entities
                    if domain in ["light", "switch", "media_player", "climate"]:
                        devices[entity_id] = {
                            "name": entity.get("attributes", {}).get("friendly_name", entity_id),
                            "type": domain,
                            "state": {
                                "state": entity["state"],
                                "attributes": entity.get("attributes", {})
                            }
                        }
                
                return devices
            else:
                logger.error(f"Error discovering Home Assistant devices: {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Error discovering Home Assistant devices: {e}")
            return {}
    
    def control_device(self, device_id: str, command: str, params: Dict = None) -> Optional[Dict]:
        """Control a Home Assistant device"""
        if params is None:
            params = {}
        
        try:
            domain = device_id.split(".")[0]
            service = None
            service_data = {"entity_id": device_id}
            
            # Map commands to Home Assistant services
            if command == "on":
                service = "turn_on"
            elif command == "off":
                service = "turn_off"
            elif command == "set_brightness" and domain == "light":
                service = "turn_on"
                service_data["brightness_pct"] = params.get("brightness", 100)
            elif command == "set_temperature" and domain == "climate":
                service = "set_temperature"
                service_data["temperature"] = params.get("temperature", 22)
            
            if not service:
                logger.error(f"Unsupported command '{command}' for {domain}")
                return None
            
            # Call the service
            url = f"{self.url}/api/services/{domain}/{service}"
            response = requests.post(url, headers=self.headers, json=service_data)
            
            if response.status_code == 200:
                # Get updated state
                time.sleep(0.5)  # Wait for state to update
                return self.get_device_state(device_id)
            else:
                logger.error(f"Error controlling Home Assistant device: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error controlling Home Assistant device: {e}")
            return None
    
    def get_device_state(self, device_id: str) -> Optional[Dict]:
        """Get Home Assistant device state"""
        try:
            url = f"{self.url}/api/states/{device_id}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                entity = response.json()
                return {
                    "state": entity["state"],
                    "attributes": entity.get("attributes", {})
                }
            else:
                logger.error(f"Error getting Home Assistant device state: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting Home Assistant device state: {e}")
            return None

# Example usage
if __name__ == "__main__":
    controller = SmartHomeController()
    
    # Print all discovered devices
    devices = controller.get_all_devices()
    print(f"Discovered {len(devices)} devices:")
    for device_id, device_info in devices.items():
        print(f"- {device_id}: {device_info['name']} ({device_info['type']})")
    
    # Print all aliases
    aliases = controller.get_all_aliases()
    print(f"\nDevice aliases:")
    for alias, device_id in aliases.items():
        print(f"- {alias} -> {device_id}")
    
    # Example: Control a device by alias
    if aliases:
        alias = list(aliases.keys())[0]
        print(f"\nTurning on {alias}...")
        result = controller.control_device(alias, "on")
        print(f"Result: {result}")
