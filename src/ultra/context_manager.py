import os
import json
import time
from typing import List, Dict
from ultra.config import APP_WORKING_DIR

# Define sessions directory in the working directory
SESSION_DIR = os.path.join(APP_WORKING_DIR, "sessions")

def ensure_session_dir():
    os.makedirs(SESSION_DIR, exist_ok=True)

class ContextManager:
    def __init__(self, session_name: str = None):
        ensure_session_dir()
        if session_name is None:
            # Create a new session name based on timestamp
            session_name = time.strftime("session-%Y%m%d-%H%M%S")
        self.session_name = session_name
        self.context = []  # List of messages

    def add_message(self, role: str, content: str):
        """
        role = "user" or "assistant" or "system"
        content = actual text
        """
        self.context.append({"role": role, "content": content})

    def clear_context(self):
        self.context = []

    def compact_context(self, provider):
        """
        Summarize the current context to reduce tokens.
        Uses a cheap model from the provider (e.g. "gpt-3.5-turbo" if available).
        """
        if not self.context:
            return

        cheap_model = provider.get_cheapest_model()  # a method we'll define
        prompt_text = (
            "Summarize the following context in a concise manner, capturing "
            "the key points and context needed to continue logically:\n\n"
        )
        for msg in self.context:
            prompt_text += f"{msg['role'].upper()}: {msg['content']}\n"

        summary = provider.get_completion(cheap_model, prompt_text)
        # Replace current context with summarized version
        self.context = [{"role": "system", "content": summary.strip()}]

    def save_session(self):
        """
        Saves context to a JSON file for future reference.
        """
        ensure_session_dir()
        file_path = os.path.join(SESSION_DIR, f"{self.session_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.context, f, indent=2)

    def export_to_text(self) -> str:
        """
        Export context as plain text.
        """
        lines = []
        for msg in self.context:
            role = msg["role"].upper()
            content = msg["content"]
            lines.append(f"{role}:\n{content}\n")
        return "\n".join(lines)
    
    
    def start_live_view(self, refresh_interval=1000):
        """
        Opens a window that updates every refresh_interval (in ms) with the current context.
        """
        try:
            import tkinter as tk
        except ImportError:
            raise ImportError(
                "Tkinter is required for the live view feature. "
                "Please ensure you are using a Python build that includes Tkinter. "
                "On macOS, consider downloading Python from python.org or installing Tcl/Tk via Homebrew."
            )
        def update_text_widget():
            text = ""
            for msg in self.context:
                text += f"{msg['role'].upper()}: {msg['content']}\n"
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, text)
            text_widget.config(state="disabled")
            root.after(refresh_interval, update_text_widget)
    
        root = tk.Tk()
        root.title("Live Context View")
        text_widget = tk.Text(root, state="disabled", width=80, height=20)
        text_widget.pack(padx=10, pady=10)
        
        update_text_widget()
        # Run the Tkinter mainloop in a separate thread to avoid blocking
        import threading
        threading.Thread(target=root.mainloop, daemon=True).start()