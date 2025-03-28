import sys
from rich.prompt import Prompt
from typing import Optional

from ultra.config import get_api_key
from ultra.context_manager import ContextManager
from ultra.providers import OpenAIProvider  # add more providers here
from ultra.utils import (
    print_ascii_art,
    print_streaming_response,
    console,
    color_text
)


class UltraApp:
    def __init__(self):
        # For demonstration, we only define an OpenAI provider. 
        # You can expand with more providers as needed.
        self.providers = {}
        self.current_provider = None
        self.current_model = None
        self.context_manager = None

    def initialize_provider(self, provider_key: str):
        """
        Creates or returns a provider object from an internal registry.
        """
        if provider_key == "openai":
            if provider_key not in self.providers:
                api_key = get_api_key(provider_key)
                self.providers[provider_key] = OpenAIProvider(api_key)
            return self.providers[provider_key]

        # Future: handle other providers
        raise ValueError(f"Unknown provider: {provider_key}")

    def select_provider_and_model(self):
        """
        Asks user to pick a provider and model from a list of available providers.
        For now, we'll do OpenAI only. You can extend to multiple providers easily.
        """
        provider_key = "openai"  # if you had multiple providers, prompt for them
        provider = self.initialize_provider(provider_key)

        console.print("\nListing available models...")
        models = provider.list_models()

        for i, m in enumerate(models):
            console.print(f"[bold cyan]{i + 1}[/bold cyan] - {m}")
        choice = Prompt.ask("\nSelect a model number", choices=[str(i + 1) for i in range(len(models))], default="1")
        model_idx = int(choice) - 1
        self.current_provider = provider
        self.current_model = models[model_idx]

    def new_session(self, session_name: Optional[str] = None):
        self.context_manager = ContextManager(session_name)

    def handle_commands(self, user_input: str) -> bool:
        """
        Returns True if command was handled (and we should skip normal prompt).
        """
        user_input = user_input.strip()

        if user_input.startswith("/new"):
            self.new_session()
            console.print("[bold green]New session started![/bold green]")
            return True

        if user_input.startswith("/clear"):
            self.context_manager.clear_context()
            console.print("[bold green]Context cleared![/bold green]")
            return True

        if user_input.startswith("/save"):
            self.context_manager.save_session()
            console.print("[bold yellow]Session saved![/bold yellow]")
            return True

        if user_input.startswith("/export"):
            txt = self.context_manager.export_to_text()
            console.print("[bold yellow]Conversation exported as text:[/bold yellow]")
            console.print(txt)
            return True

        if user_input.startswith("/compact"):
            self.context_manager.compact_context(self.current_provider)
            console.print("[bold green]Context summarized/compacted![/bold green]")
            return True

        if user_input.startswith("/model"):
            console.print("[bold magenta]Switching model...[/bold magenta]")
            self.select_provider_and_model()
            return True

        if user_input in ("/quit", "/exit"):
            console.print("[bold red]Goodbye![/bold red]")
            sys.exit(0)

        return False

    def chat_loop(self):
        """
        Primary chat loop after a model is selected.
        """
        # Use #000000 for true black instead of default bold black which might appear as gray
        console.print(f"[bold #000000]Ultra CLI - Quick Chat with {self.current_model}[/bold #000000]\n")
        while True:
            # Prompt for user input (without extra line space)
            user_prompt = console.input(color_text("John >>> ", "blue"))

            # Check if input is a command
            if user_prompt.startswith("/"):
                handled = self.handle_commands(user_prompt)
                if handled:
                    continue

            # Add user message to context
            self.context_manager.add_message("user", user_prompt)

            # Add an empty line between messages
            print()
            
            # Prepare context for model
            messages = self.context_manager.context
            console.print(color_text("Ultra >>>", "red"), end=" ")
            # Stream the model's response
            full_response = print_streaming_response(self.current_provider, self.current_model, messages)
            console.print()  # Add a newline after the streamed response

            self.context_manager.add_message("assistant", full_response)

def run_interactive_welcome():
    """
    Called when user types 'ultra models'.
    """
    # Set terminal title (no newline)
    print("\033]0;⚡ Ultra Chat\007", end="")
    
    # Show ASCII art for 'ultra models' command
    print_ascii_art()
    
    # Show welcome message
    console.print("Welcome to Ultra CLI. Type /quit at any time to exit.\n")
    
    app = UltraApp()
    app.select_provider_and_model()
    app.new_session()
    app.chat_loop()