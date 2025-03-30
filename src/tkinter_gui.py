import tkinter as tk
from tkinter import ttk, scrolledtext
from chatbot import TelecomChatbot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TelecomChatbotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Telecom Support Chatbot")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize chatbot
        self.chatbot = TelecomChatbot()
        self.user_id = None
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", padding=10, font=("Helvetica", 10))
        self.style.configure("Custom.TEntry", padding=5, font=("Helvetica", 10))
        
        # Create main container
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(1, weight=1)
        
        # Create login frame
        self.login_frame = ttk.Frame(self.main_container)
        self.login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Login components
        ttk.Label(self.login_frame, text="User ID:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.user_id_entry = ttk.Entry(self.login_frame, width=30, style="Custom.TEntry")
        self.user_id_entry.grid(row=0, column=1, padx=5)
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login, style="Custom.TButton")
        self.login_button.grid(row=0, column=2, padx=5)
        
        # Create chat frame
        self.chat_frame = ttk.Frame(self.main_container)
        self.chat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Configure chat frame grid
        self.chat_frame.columnconfigure(0, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)
        
        # Chat display area with custom styling
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Helvetica", 10),
            bg="white",
            fg="#333333"
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Message input area
        self.message_frame = ttk.Frame(self.chat_frame)
        self.message_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.message_frame.columnconfigure(0, weight=1)
        
        self.message_entry = ttk.Entry(self.message_frame, style="Custom.TEntry")
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)
        
        # Buttons frame
        self.buttons_frame = ttk.Frame(self.chat_frame)
        self.buttons_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Action buttons
        self.send_button = ttk.Button(
            self.message_frame,
            text="Send",
            command=self.send_message,
            style="Custom.TButton"
        )
        self.send_button.grid(row=0, column=1, padx=5)
        
        self.clear_button = ttk.Button(
            self.buttons_frame,
            text="Clear Chat",
            command=self.clear_chat,
            style="Custom.TButton"
        )
        self.clear_button.grid(row=0, column=0, padx=5)
        
        self.logout_button = ttk.Button(
            self.buttons_frame,
            text="Logout",
            command=self.logout,
            style="Custom.TButton"
        )
        self.logout_button.grid(row=0, column=1, padx=5)
        
        # Initially hide chat components
        self.hide_chat_components()
        
        # Bind Enter key to send message
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        # Add welcome message
        self.chat_display.insert(tk.END, "Welcome to Telecom Support Chatbot!\n")
        self.chat_display.insert(tk.END, "Please enter your User ID to continue.\n\n")
        self.chat_display.config(state=tk.DISABLED)
        
    def login(self):
        user_id = self.user_id_entry.get().strip()
        if user_id:
            self.user_id = user_id
            self.show_chat_components()
            self.hide_login_components()
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.insert(tk.END, f"Welcome, {user_id}! How can I help you today?\n\n")
            self.chat_display.config(state=tk.DISABLED)
            self.message_entry.focus()
        else:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, "Please enter a valid User ID.\n\n")
            self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self):
        message = self.message_entry.get().strip()
        if message and self.user_id:
            # Display user message
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"You: {message}\n")
            
            # Get and display bot response
            response = self.chatbot.process_message(message, self.user_id)
            self.chat_display.insert(tk.END, f"Bot: {response}\n\n")
            
            # Clear message entry
            self.message_entry.delete(0, tk.END)
            
            # Save conversation
            self.chatbot.db.save_conversation(self.user_id, message, response)
            
            # Disable chat display
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
    
    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.insert(tk.END, f"Welcome, {self.user_id}! How can I help you today?\n\n")
        self.chat_display.config(state=tk.DISABLED)
    
    def logout(self):
        self.user_id = None
        self.hide_chat_components()
        self.show_login_components()
        self.user_id_entry.delete(0, tk.END)
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.insert(tk.END, "Welcome to Telecom Support Chatbot!\n")
        self.chat_display.insert(tk.END, "Please enter your User ID to continue.\n\n")
        self.chat_display.config(state=tk.DISABLED)
    
    def show_chat_components(self):
        self.chat_frame.grid()
        self.message_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)
        self.logout_button.config(state=tk.NORMAL)
    
    def hide_chat_components(self):
        self.chat_frame.grid_remove()
        self.message_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)
        self.logout_button.config(state=tk.DISABLED)
    
    def show_login_components(self):
        self.login_frame.grid()
        self.user_id_entry.config(state=tk.NORMAL)
        self.login_button.config(state=tk.NORMAL)
    
    def hide_login_components(self):
        self.login_frame.grid_remove()
        self.user_id_entry.config(state=tk.DISABLED)
        self.login_button.config(state=tk.DISABLED)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TelecomChatbotGUI()
    app.run() 