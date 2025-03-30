import tkinter as tk
from tkinter import ttk, scrolledtext
from chatbot import TelecomChatbot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TelecomChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Telecom Customer Service Chatbot")
        self.root.geometry("800x600")
        
        # Initialize chatbot
        self.chatbot = TelecomChatbot()
        self.user_id = None
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Login frame
        self.login_frame = ttk.Frame(self.main_frame)
        self.login_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(self.login_frame, text="User ID:").grid(row=0, column=0, padx=5)
        self.user_id_entry = ttk.Entry(self.login_frame, width=30)
        self.user_id_entry.grid(row=0, column=1, padx=5)
        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=0, column=2, padx=5)
        
        # Chat frame
        self.chat_frame = ttk.Frame(self.main_frame)
        self.chat_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Message input
        self.message_entry = ttk.Entry(self.chat_frame)
        self.message_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(self.chat_frame, text="Send", command=self.send_message).grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(self.button_frame, text="Clear Chat", command=self.clear_chat).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Logout", command=self.logout).grid(row=0, column=1, padx=5)
        
        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.chat_frame.columnconfigure(0, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)
        
        # Bind Enter key to send message
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        
        # Initially hide chat interface
        self.chat_frame.grid_remove()
        self.button_frame.grid_remove()

    def login(self):
        user_id = self.user_id_entry.get().strip()
        if user_id:
            self.user_id = user_id
            self.login_frame.grid_remove()
            self.chat_frame.grid()
            self.button_frame.grid()
            self.chat_display.insert(tk.END, f"Welcome, {user_id}! How can I help you today?\n\n")
            self.message_entry.focus()

    def send_message(self):
        if not self.user_id:
            return
            
        message = self.message_entry.get().strip()
        if message:
            # Display user message
            self.chat_display.insert(tk.END, f"You: {message}\n")
            
            # Get bot response
            response = self.chatbot.process_message(self.user_id, message)
            
            # Display bot response
            self.chat_display.insert(tk.END, f"Bot: {response}\n\n")
            
            # Clear input and scroll to bottom
            self.message_entry.delete(0, tk.END)
            self.chat_display.see(tk.END)

    def clear_chat(self):
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.insert(tk.END, f"Welcome back, {self.user_id}! How can I help you today?\n\n")

    def logout(self):
        self.user_id = None
        self.user_id_entry.delete(0, tk.END)
        self.message_entry.delete(0, tk.END)
        self.chat_display.delete(1.0, tk.END)
        self.chat_frame.grid_remove()
        self.button_frame.grid_remove()
        self.login_frame.grid()
        self.user_id_entry.focus()

def main():
    root = tk.Tk()
    app = TelecomChatbotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 