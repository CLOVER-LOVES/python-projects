"""
Voice Assistant GUI Interface
----------------------------
This module provides a graphical user interface for the voice assistant.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
import os
import json
from PIL import Image, ImageTk
import enhanced_voice_assistant as va

class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Set theme and style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern theme
        
        # Define colors
        self.bg_color = "#f5f5f5"
        self.accent_color = "#4a6ea9"
        self.text_color = "#333333"
        self.highlight_color = "#6d8cc7"
        
        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TButton', 
                             background=self.accent_color, 
                             foreground='white', 
                             padding=10,
                             font=('Helvetica', 10))
        self.style.map('TButton', 
                       background=[('active', self.highlight_color)])
        self.style.configure('TLabel', 
                             background=self.bg_color, 
                             foreground=self.text_color,
                             font=('Helvetica', 11))
        self.style.configure('Header.TLabel', 
                             font=('Helvetica', 16, 'bold'))
        
        # Set root background
        self.root.configure(bg=self.bg_color)
        
        # Create message queue for thread-safe communication
        self.message_queue = queue.Queue()
        
        # Initialize assistant in a separate thread
        self.assistant = None
        self.assistant_thread = None
        self.is_listening = False
        self.is_running = True
        
        # Create the GUI elements
        self.create_widgets()
        
        # Start checking the message queue
        self.check_queue()
        
        # Initialize the assistant
        self.initialize_assistant()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = ttk.Label(self.header_frame, 
                                     text="Voice Assistant", 
                                     style='Header.TLabel')
        self.title_label.pack(side=tk.LEFT)
        
        # Status indicator
        self.status_frame = ttk.Frame(self.header_frame)
        self.status_frame.pack(side=tk.RIGHT)
        
        self.status_label = ttk.Label(self.status_frame, text="Status: ")
        self.status_label.pack(side=tk.LEFT)
        
        self.status_indicator = tk.Canvas(self.status_frame, 
                                         width=15, 
                                         height=15, 
                                         bg=self.bg_color,
                                         highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT)
        self.status_indicator.create_oval(2, 2, 13, 13, fill="gray", outline="")
        
        # Conversation display
        self.conversation_frame = ttk.Frame(self.main_frame)
        self.conversation_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.conversation_display = scrolledtext.ScrolledText(
            self.conversation_frame,
            wrap=tk.WORD,
            font=('Helvetica', 10),
            bg='white',
            fg=self.text_color
        )
        self.conversation_display.pack(fill=tk.BOTH, expand=True)
        self.conversation_display.config(state=tk.DISABLED)
        
        # Control buttons
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.listen_button = ttk.Button(
            self.control_frame, 
            text="Start Listening",
            command=self.toggle_listening
        )
        self.listen_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.settings_button = ttk.Button(
            self.control_frame, 
            text="Settings",
            command=self.open_settings
        )
        self.settings_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.exit_button = ttk.Button(
            self.control_frame, 
            text="Exit",
            command=self.exit_application
        )
        self.exit_button.pack(side=tk.RIGHT)
    
    def initialize_assistant(self):
        """Initialize the voice assistant in a separate thread"""
        def init_thread():
            try:
                self.update_status("Initializing...", "orange")
                self.add_message("System", "Initializing voice assistant...")
                self.assistant = va.VoiceAssistant()
                
                # Override the speak method to update the GUI
                original_speak = self.assistant.speak
                def gui_speak(text):
                    self.message_queue.put(("Assistant", text))
                    original_speak(text)
                self.assistant.speak = gui_speak
                
                # Override the take_command method
                original_take_command = self.assistant.take_command
                def gui_take_command():
                    if self.is_listening:
                        self.update_status("Listening...", "green")
                        result = original_take_command()
                        self.update_status("Processing...", "orange")
                        if result:
                            self.message_queue.put(("You", result))
                        self.update_status("Ready", "blue")
                        return result
                    return None
                self.assistant.take_command = gui_take_command
                
                # Initialization complete
                self.message_queue.put(("System", "Voice assistant initialized and ready!"))
                self.update_status("Ready", "blue")
            except Exception as e:
                self.message_queue.put(("Error", f"Failed to initialize assistant: {str(e)}"))
                self.update_status("Error", "red")
        
        # Start the initialization thread
        init_thread = threading.Thread(target=init_thread)
        init_thread.daemon = True
        init_thread.start()
    
    def start_assistant_loop(self):
        """Start the main assistant loop in a separate thread"""
        if self.assistant_thread is not None and self.assistant_thread.is_alive():
            return  # Already running
        
        def assistant_loop():
            try:
                while self.is_running:
                    if self.is_listening and self.assistant:
                        query = self.assistant.take_command()
                        if query:
                            if 'exit' in query or 'quit' in query or 'goodbye' in query:
                                self.message_queue.put(("System", "Exiting voice assistant..."))
                                self.is_listening = False
                                self.root.after(0, self.update_listen_button)
                                break
                            self.assistant.process_command(query)
                    time.sleep(0.1)  # Small delay to prevent high CPU usage
            except Exception as e:
                self.message_queue.put(("Error", f"Assistant error: {str(e)}"))
                self.update_status("Error", "red")
        
        # Start the assistant thread
        self.assistant_thread = threading.Thread(target=assistant_loop)
        self.assistant_thread.daemon = True
        self.assistant_thread.start()
    
    def toggle_listening(self):
        """Toggle the listening state"""
        if not self.assistant:
            messagebox.showinfo("Not Ready", "The assistant is still initializing. Please wait.")
            return
        
        self.is_listening = not self.is_listening
        
        if self.is_listening:
            self.listen_button.config(text="Stop Listening")
            self.update_status("Listening...", "green")
            if not self.assistant_thread or not self.assistant_thread.is_alive():
                self.start_assistant_loop()
        else:
            self.listen_button.config(text="Start Listening")
            self.update_status("Ready", "blue")
    
    def update_listen_button(self):
        """Update the listen button text based on listening state"""
        if self.is_listening:
            self.listen_button.config(text="Stop Listening")
        else:
            self.listen_button.config(text="Start Listening")
    
    def update_status(self, status_text, color):
        """Update the status indicator"""
        self.message_queue.put(("status", (status_text, color)))
    
    def open_settings(self):
        """Open the settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.minsize(400, 300)
        settings_window.configure(bg=self.bg_color)
        
        # Make it modal
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings container
        settings_frame = ttk.Frame(settings_window)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(settings_frame, 
                               text="Assistant Settings", 
                               style='Header.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Settings options
        # Voice selection
        voice_frame = ttk.Frame(settings_frame)
        voice_frame.pack(fill=tk.X, pady=(0, 10))
        
        voice_label = ttk.Label(voice_frame, text="Voice:")
        voice_label.pack(side=tk.LEFT)
        
        voice_var = tk.StringVar(value="Male" if self.assistant and self.assistant.config['voice'] == 0 else "Female")
        voice_male = ttk.Radiobutton(voice_frame, text="Male", variable=voice_var, value="Male")
        voice_male.pack(side=tk.LEFT, padx=(10, 5))
        
        voice_female = ttk.Radiobutton(voice_frame, text="Female", variable=voice_var, value="Female")
        voice_female.pack(side=tk.LEFT)
        
        # Weather API
        weather_frame = ttk.Frame(settings_frame)
        weather_frame.pack(fill=tk.X, pady=(0, 10))
        
        weather_label = ttk.Label(weather_frame, text="Weather API Key:")
        weather_label.pack(anchor=tk.W)
        
        weather_var = tk.StringVar(value=self.assistant.config.get('weather_api_key', '') if self.assistant else '')
        weather_entry = ttk.Entry(weather_frame, textvariable=weather_var, width=40)
        weather_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Music directory
        music_frame = ttk.Frame(settings_frame)
        music_frame.pack(fill=tk.X, pady=(0, 10))
        
        music_label = ttk.Label(music_frame, text="Music Directory:")
        music_label.pack(anchor=tk.W)
        
        music_var = tk.StringVar(value=self.assistant.config['paths'].get('music_dir', '') if self.assistant else '')
        music_entry = ttk.Entry(music_frame, textvariable=music_var, width=40)
        music_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Email settings
        email_frame = ttk.Frame(settings_frame)
        email_frame.pack(fill=tk.X, pady=(0, 10))
        
        email_label = ttk.Label(email_frame, text="Email Settings:")
        email_label.pack(anchor=tk.W)
        
        email_sender_frame = ttk.Frame(email_frame)
        email_sender_frame.pack(fill=tk.X, pady=(5, 0))
        
        email_sender_label = ttk.Label(email_sender_frame, text="Email:")
        email_sender_label.pack(side=tk.LEFT)
        
        email_sender_var = tk.StringVar(value=self.assistant.config['email'].get('sender', '') if self.assistant else '')
        email_sender_entry = ttk.Entry(email_sender_frame, textvariable=email_sender_var, width=30)
        email_sender_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        email_password_frame = ttk.Frame(email_frame)
        email_password_frame.pack(fill=tk.X, pady=(5, 0))
        
        email_password_label = ttk.Label(email_password_frame, text="Password:")
        email_password_label.pack(side=tk.LEFT)
        
        email_password_var = tk.StringVar(value=self.assistant.config['email'].get('password', '') if self.assistant else '')
        email_password_entry = ttk.Entry(email_password_frame, textvariable=email_password_var, width=30, show="*")
        email_password_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def save_settings():
            if not self.assistant:
                messagebox.showinfo("Not Ready", "The assistant is still initializing. Please wait.")
                return
            
            try:
                # Update configuration
                self.assistant.config['voice'] = 0 if voice_var.get() == "Male" else 1
                self.assistant.config['weather_api_key'] = weather_var.get()
                self.assistant.config['paths']['music_dir'] = music_var.get()
                self.assistant.config['email']['sender'] = email_sender_var.get()
                self.assistant.config['email']['password'] = email_password_var.get()
                
                # Save to file
                self.assistant.save_config()
                
                # Update voice if needed
                if self.assistant.engine.getProperty('voice') != self.assistant.voices[self.assistant.config['voice']].id:
                    self.assistant.engine.setProperty('voice', self.assistant.voices[self.assistant.config['voice']].id)
                
                messagebox.showinfo("Settings Saved", "Your settings have been saved successfully.")
                settings_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
        
        save_button = ttk.Button(button_frame, text="Save", command=save_settings)
        save_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_button = ttk.Button(button_frame, text="Cancel", command=settings_window.destroy)
        cancel_button.pack(side=tk.RIGHT)
    
    def add_message(self, sender, message):
        """Add a message to the conversation display"""
        self.conversation_display.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        
        # Format based on sender
        if sender == "System":
            self.conversation_display.insert(tk.END, f"[{timestamp}] ", "time")
            self.conversation_display.insert(tk.END, f"{message}\n\n", "system")
        elif sender == "Error":
            self.conversation_display.insert(tk.END, f"[{timestamp}] ", "time")
            self.conversation_display.insert(tk.END, f"ERROR: {message}\n\n", "error")
        elif sender == "You":
            self.conversation_display.insert(tk.END, f"[{timestamp}] ", "time")
            self.conversation_display.insert(tk.END, f"You: ", "you")
            self.conversation_display.insert(tk.END, f"{message}\n", "you_message")
        elif sender == "Assistant":
            self.conversation_display.insert(tk.END, f"[{timestamp}] ", "time")
            self.conversation_display.insert(tk.END, f"Assistant: ", "assistant")
            self.conversation_display.insert(tk.END, f"{message}\n\n", "assistant_message")
        
        # Configure tags
        self.conversation_display.tag_configure("time", foreground="gray")
        self.conversation_display.tag_configure("system", foreground="purple")
        self.conversation_display.tag_configure("error", foreground="red")
        self.conversation_display.tag_configure("you", foreground="blue", font=('Helvetica', 10, 'bold'))
        self.conversation_display.tag_configure("you_message", foreground="blue")
        self.conversation_display.tag_configure("assistant", foreground="green", font=('Helvetica', 10, 'bold'))
        self.conversation_display.tag_configure("assistant_message", foreground="green")
        
        # Scroll to the end
        self.conversation_display.see(tk.END)
        self.conversation_display.config(state=tk.DISABLED)
    
    def check_queue(self):
        """Check the message queue for updates from the assistant thread"""
        try:
            while not self.message_queue.empty():
                message = self.message_queue.get(0)
                
                # Handle different message types
                if message[0] == "status":
                    status_text, color = message[1]
                    self.status_label.config(text=f"Status: {status_text}")
                    self.status_indicator.delete("all")
                    self.status_indicator.create_oval(2, 2, 13, 13, fill=color, outline="")
                else:
                    self.add_message(message[0], message[1])
        except Exception as e:
            print(f"Error in check_queue: {e}")
        
        # Schedule the next check
        self.root.after(100, self.check_queue)
    
    def exit_application(self):
        """Safely exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.is_running = False
            self.is_listening = False
            self.root.destroy()

def main():
    """Main function to start the GUI"""
    root = tk.Tk()
    app = AssistantGUI(root)
    
    # Set window icon if available
    try:
        root.iconbitmap("assistant_icon.ico")
    except:
        pass  # Icon not found, use default
    
    root.mainloop()

if __name__ == "__main__":
    main()
