import sys
import os
import importlib

def main():
    """
    Parses CLI args and delegates to the appropriate run mode.
    """
    # Only import necessary modules when needed
    from ultra.config import APP_WORKING_DIR
    
    args = sys.argv[1:]
    
    if len(args) == 0:
        # No subcommands => Show quick start with default model
        # Set terminal title (no newline)
        print("\033]0;⚡ Ultra Chat\007", end="")
        # Switch to the configured working directory
        os.chdir(APP_WORKING_DIR)
        
        # Lazy load modules only when needed
        from ultra.logging_config import configure_logging
        from ultra.app import UltraApp
        from ultra.utils import console
        
        # Create app without initial message (will show in chat_loop with model)
        configure_logging()
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
        # Switch to the configured working directory
        os.chdir(APP_WORKING_DIR)
        
        # Lazy load modules only when needed
        from ultra.app import UltraApp
        
        # Create app without initial message (will show in chat_loop with model)
        app = UltraApp()
        provider = app.initialize_provider("openai")
        app.current_provider = provider
        app.current_model = provider.get_cheapest_model()
        app.new_session()
        app.chat_loop()
    elif subcommand == "--help" or subcommand == "-h":
        # Import only the console for help display
        from ultra.utils import console
        console.print("\n[bold]Ultra CLI[/bold] - A tool for chat and transcription\n")
        console.print("Commands:")
        console.print("  [cyan]ultra[/cyan]             Start a quick chat session")
        console.print("  [cyan]ultra chat[/cyan]        Start a chat session")
        console.print("  [cyan]ultra models[/cyan]      Choose from available models")
        console.print("  [cyan]ultra --help[/cyan]      Show this help message\n")
    else:
        # Import only the console for error display
        from ultra.utils import console
        console.print(f"[red]Unknown command: {subcommand}[/red]")
        console.print("Available commands: models / chat / --help")