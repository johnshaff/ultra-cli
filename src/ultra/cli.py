import sys
import os
from rich.console import Console

from ultra.app import UltraApp
from ultra.utils import print_ascii_art, console

def main():
    """
    Parses CLI args and delegates to the appropriate run mode.
    """
    args = sys.argv[1:]
    
    if len(args) == 0:
        # No subcommands => Show quick start with default model
        # Set terminal title (no newline)
        print("\033]0;⚡ Ultra Chat\007", end="")
        # Create app without initial message (will show in chat_loop with model)
        app = UltraApp()
        provider = app.initialize_provider("openai")
        app.current_provider = provider
        app.current_model = provider.get_cheapest_model()
        app.new_session()
        app.chat_loop()
        return

    subcommand = args[0]
    if subcommand == "models":
        # Show welcome + model selection
        from ultra.app import run_interactive_welcome
        run_interactive_welcome()
    elif subcommand == "chat":
        # Set terminal title (no newline)
        print("\033]0;⚡ Ultra Chat\007", end="")
        # Create app without initial message (will show in chat_loop with model)
        app = UltraApp()
        provider = app.initialize_provider("openai")
        app.current_provider = provider
        app.current_model = provider.get_cheapest_model()
        app.new_session()
        app.chat_loop()
    else:
        console.print(f"[red]Unknown command: {subcommand}[/red]")
        console.print("Available commands: models / chat")