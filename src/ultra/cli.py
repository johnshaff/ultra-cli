import sys
from rich.console import Console

from ultra.app import UltraApp
from ultra.utils import print_ascii_art, console

def main():
    """
    Parses CLI args and delegates to the appropriate run mode.
    """
    args = sys.argv[1:]
    
    if len(args) == 0:
        # No subcommands => Show welcome + model selection
        from ultra.app import run_interactive_welcome
        run_interactive_welcome()
        return

    subcommand = args[0]
    if subcommand == "chat":
        # Start chat with default model
        console.print("[bold magenta]Ultra CLI - Quick Chat[/bold magenta]")
        app = UltraApp()
        # We'll skip the selection and pick a default
        # e.g. "openai" with "gpt-3.5-turbo"
        provider = app.initialize_provider("openai")
        app.current_provider = provider
        app.current_model = provider.get_cheapest_model()
        app.new_session()
        app.chat_loop()
    else:
        console.print(f"[red]Unknown command: {subcommand}[/red]")
        console.print("Available commands: (none) / chat")