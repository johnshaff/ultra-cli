from rich.console import Console
from rich.markdown import Markdown

console = Console()

def print_ascii_art():
    art = r"""
██╗   ██╗██╗  ████████╗██████╗  █████╗ 
██║   ██║██║  ╚══██╔══╝██╔══██╗██╔══██╗
██║   ██║██║     ██║   ██████╔╝███████║
╚██╗ ██╔╝██║     ██║   ██╔══██╗██╔══██║
 ╚████╔╝ ███████╗██║   ██║  ██║██║  ██║
  ╚═══╝  ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
    """
    console.print(art, style="bold magenta")

def color_text(text: str, style: str) -> str:
    """
    Return text styled for the console, e.g. "blue", "red", "bold green", etc.
    """
    return f"[{style}]{text}[/{style}]"

def print_streaming_response(provider, model_name, messages):
    """
    Streams the model's response token by token.
    """
    for token in provider.stream_completion(model_name, messages):
        # Use print with flush=True instead of console.print
        print(token, end="", flush=True)
    print()  # move to next line

def print_markdown(md_text: str):
    """
    Print multi-line text as markdown (code highlighting, etc.) using Rich.
    """
    markdown_obj = Markdown(md_text)
    console.print(markdown_obj)