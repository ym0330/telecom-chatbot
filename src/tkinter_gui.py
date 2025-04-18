import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from chatbot import TelecomChatbot
import os
from dotenv import load_dotenv
from auth import Auth

# Load environment variables
load_dotenv()

class TelecomChatbotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Telecom Support Chatbot")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize chatbot and auth
        self.chatbot = TelecomChatbot()
        self.auth = Auth()
        self.current_user = None
        
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
        
        # Create auth frame
        self.auth_frame = ttk.Frame(self.main_container)
        self.auth_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Create login frame
        self.login_frame = ttk.Frame(self.auth_frame)
        self.login_frame.grid(row=0, column=0, padx=5)
        
        # Login components
        ttk.Label(self.login_frame, text="Username:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.username_entry = ttk.Entry(self.login_frame, width=30, style="Custom.TEntry")
        self.username_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(self.login_frame, text="Password:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5)
        self.password_entry = ttk.Entry(self.login_frame, width=30, style="Custom.TEntry", show="*")
        self.password_entry.grid(row=1, column=1, padx=5)
        
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login, style="Custom.TButton")
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Create register frame
        self.register_frame = ttk.Frame(self.auth_frame)
        self.register_frame.grid(row=1, column=0, padx=5)
        
        # Register components
        ttk.Label(self.register_frame, text="New User Registration", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(self.register_frame, text="Username:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5)
        self.reg_username_entry = ttk.Entry(self.register_frame, width=30, style="Custom.TEntry")
        self.reg_username_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(self.register_frame, text="Email:", font=("Helvetica", 12)).grid(row=2, column=0, padx=5)
        self.email_entry = ttk.Entry(self.register_frame, width=30, style="Custom.TEntry")
        self.email_entry.grid(row=2, column=1, padx=5)
        
        ttk.Label(self.register_frame, text="Password:", font=("Helvetica", 12)).grid(row=3, column=0, padx=5)
        self.reg_password_entry = ttk.Entry(self.register_frame, width=30, style="Custom.TEntry", show="*")
        self.reg_password_entry.grid(row=3, column=1, padx=5)
        
        ttk.Label(self.register_frame, text="Confirm Password:", font=("Helvetica", 12)).grid(row=4, column=0, padx=5)
        self.confirm_password_entry = ttk.Entry(self.register_frame, width=30, style="Custom.TEntry", show="*")
        self.confirm_password_entry.grid(row=4, column=1, padx=5)
        
        self.register_button = ttk.Button(self.register_frame, text="Register", command=self.register, style="Custom.TButton")
        self.register_button.grid(row=5, column=0, columnspan=2, pady=10)
        
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
        self.chat_display.insert(tk.END, "Please login or register to continue.\n\n")
        self.chat_display.config(state=tk.DISABLED)
    
    def register(self):
        username = self.reg_username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not all([username, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        success, message = self.auth.register_user(username, password, email)
        if success:
            messagebox.showinfo("Success", message)
            # Clear registration fields
            self.reg_username_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.reg_password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            # Switch to login
            self.username_entry.insert(0, username)
            self.password_entry.insert(0, password)
            self.login()
        else:
            messagebox.showerror("Error", message)
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        success, message, user_data = self.auth.login_user(username, password)
        if success:
            self.current_user = user_data
            self.show_chat_components()
            self.hide_auth_components()
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.insert(tk.END, f"Welcome, {username}! How can I help you today?\n\n")
            self.chat_display.config(state=tk.DISABLED)
            self.message_entry.focus()
        else:
            messagebox.showerror("Error", message)
    
    def send_message(self):
        message = self.message_entry.get().strip()
        if message and self.current_user:
            # Display user message
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"You: {message}\n")
            
            # Get and display bot response
            response = self.chatbot.process_message(message, self.current_user['username'])
            self.chat_display.insert(tk.END, f"Bot: {response}\n\n")
            
            # Clear message entry
            self.message_entry.delete(0, tk.END)
            
            # Save conversation
            self.chatbot.db.save_conversation(self.current_user['username'], message, response)
            
            # Disable chat display
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
    
    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.insert(tk.END, f"Welcome, {self.current_user['username']}! How can I help you today?\n\n")
        self.chat_display.config(state=tk.DISABLED)
    
    def logout(self):
        self.current_user = None
        self.hide_chat_components()
        self.show_auth_components()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.insert(tk.END, "Welcome to Telecom Support Chatbot!\n")
        self.chat_display.insert(tk.END, "Please login or register to continue.\n\n")
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
    
    def show_auth_components(self):
        self.auth_frame.grid()
        self.username_entry.config(state=tk.NORMAL)
        self.password_entry.config(state=tk.NORMAL)
        self.login_button.config(state=tk.NORMAL)
        self.reg_username_entry.config(state=tk.NORMAL)
        self.email_entry.config(state=tk.NORMAL)
        self.reg_password_entry.config(state=tk.NORMAL)
        self.confirm_password_entry.config(state=tk.NORMAL)
        self.register_button.config(state=tk.NORMAL)
    
    def hide_auth_components(self):
        self.auth_frame.grid_remove()
        self.username_entry.config(state=tk.DISABLED)
        self.password_entry.config(state=tk.DISABLED)
        self.login_button.config(state=tk.DISABLED)
        self.reg_username_entry.config(state=tk.DISABLED)
        self.email_entry.config(state=tk.DISABLED)
        self.reg_password_entry.config(state=tk.DISABLED)
        self.confirm_password_entry.config(state=tk.DISABLED)
        self.register_button.config(state=tk.DISABLED)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TelecomChatbotGUI()
    app.run() 