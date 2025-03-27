import os
import json
import time
from typing import List, Dict

SESSION_DIR = os.path.join(os.path.expanduser("~"), ".ultra", "sessions")

def ensure_session_dir():
    os.makedirs(SESSION_DIR, exist_ok=True)

class ContextManager:
    def __init__(self, session_name: str = None):
        ensure_session_dir()
        if session_name is None:
            # Create a new session name based on timestamp
            session_name = time.strftime("session-%Y%m%d-%H%M%S")
        self.session_name = session_name
        self.conversation = []  # List of messages

    def add_message(self, role: str, content: str):
        """
        role = "user" or "assistant" or "system"
        content = actual text
        """
        self.conversation.append({"role": role, "content": content})

    def clear_context(self):
        self.conversation = []

    def compact_context(self, provider):
        """
        Summarize the current conversation to reduce tokens.
        Uses a cheap model from the provider (e.g. "gpt-3.5-turbo" if available).
        """
        if not self.conversation:
            return

        cheap_model = provider.get_cheapest_model()  # a method we'll define
        prompt_text = (
            "Summarize the following conversation in a concise manner, capturing "
            "the key points and context needed to continue logically:\n\n"
        )
        for msg in self.conversation:
            prompt_text += f"{msg['role'].upper()}: {msg['content']}\n"

        summary = provider.get_completion(cheap_model, prompt_text)
        # Replace current context with summarized version
        self.conversation = [{"role": "system", "content": summary.strip()}]

    def save_session(self):
        """
        Saves conversation to a JSON file for future reference.
        """
        ensure_session_dir()
        file_path = os.path.join(SESSION_DIR, f"{self.session_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.conversation, f, indent=2)

    def export_to_text(self) -> str:
        """
        Export conversation as plain text.
        """
        lines = []
        for msg in self.conversation:
            role = msg["role"].upper()
            content = msg["content"]
            lines.append(f"{role}:\n{content}\n")
        return "\n".join(lines)