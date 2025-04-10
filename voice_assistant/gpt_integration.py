"""
OpenAI GPT Integration Module
---------------------------
This module provides integration with OpenAI's GPT models for more natural conversations.
"""

import os
import json
import logging
import time
import openai
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GPTAssistant:
    """
    Integration with OpenAI's GPT models for conversational AI
    """
    def __init__(self, api_key=None, model="gpt-3.5-turbo", conversation_file="conversation_history.json"):
        """
        Initialize the GPT assistant.
        
        Args:
            api_key (str): OpenAI API key
            model (str): GPT model to use
            conversation_file (str): File to store conversation history
        """
        self.api_key = api_key
        self.model = model
        self.conversation_file = conversation_file
        self.conversation_history = []
        self.max_history = 10  # Maximum number of exchanges to keep in history
        self.system_message = {
            "role": "system", 
            "content": (
                "You are a helpful voice assistant. "
                "Provide concise, helpful responses. "
                "If you don't know something, say so. "
                "For complex topics, offer a brief summary. "
                "For tasks the user wants to perform, explain how you can help."
            )
        }
        
        # Load conversation history if available
        self.load_conversation_history()
    
    def load_conversation_history(self):
        """Load conversation history from file"""
        try:
            if os.path.exists(self.conversation_file):
                with open(self.conversation_file, 'r') as f:
                    self.conversation_history = json.load(f)
                logger.info(f"Loaded {len(self.conversation_history)} conversation exchanges")
        except Exception as e:
            logger.error(f"Failed to load conversation history: {e}")
            self.conversation_history = []
    
    def save_conversation_history(self):
        """Save conversation history to file"""
        try:
            # Limit the history size
            if len(self.conversation_history) > self.max_history * 2:  # Each exchange is 2 messages
                self.conversation_history = self.conversation_history[-(self.max_history * 2):]
            
            with open(self.conversation_file, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save conversation history: {e}")
    
    def get_response(self, user_input: str) -> Optional[str]:
        """
        Get a response from the GPT model.
        
        Args:
            user_input (str): User's input text
            
        Returns:
            str: GPT's response or None if an error occurred
        """
        if not self.api_key:
            logger.error("API key not provided")
            return "I'm sorry, but I'm not configured with an API key to access my language capabilities."
        
        try:
            # Set the API key
            openai.api_key = self.api_key
            
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Prepare messages for API call
            messages = [self.system_message] + self.conversation_history[-self.max_history * 2:]
            
            # Call the OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=150,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content.strip()
            
            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            # Save updated history
            self.save_conversation_history()
            
            return response_text
        
        except openai.error.RateLimitError:
            logger.error("Rate limit exceeded")
            return "I'm sorry, but I've reached my rate limit. Please try again in a moment."
        
        except openai.error.AuthenticationError:
            logger.error("Authentication error")
            return "I'm sorry, but there's an issue with my API authentication. Please check my configuration."
        
        except Exception as e:
            logger.error(f"Error getting GPT response: {e}")
            return "I'm sorry, but I encountered an error while processing your request."
    
    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        self.save_conversation_history()
        logger.info("Conversation history cleared")
    
    def update_system_message(self, new_system_message: str):
        """
        Update the system message that guides the assistant's behavior.
        
        Args:
            new_system_message (str): New system message
        """
        self.system_message = {"role": "system", "content": new_system_message}
        logger.info("System message updated")

# Example usage
if __name__ == "__main__":
    # Replace with your OpenAI API key
    api_key = "YOUR_OPENAI_API_KEY"
    
    assistant = GPTAssistant(api_key=api_key)
    
    print("GPT Assistant initialized. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response = assistant.get_response(user_input)
        print(f"Assistant: {response}")
