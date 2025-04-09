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