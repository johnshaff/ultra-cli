from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live


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
    console.print(art, style="bold magenta", end="")

def color_text(text: str, style: str) -> str:
    """
    Return text styled for the console, e.g. "blue", "red", "bold green", etc.
    """
    return f"[{style}]{text}[/{style}]"

def print_streaming_response(provider, model_name, messages) -> str:
    """
    Streams the model's response token by token and returns the full text.
    """
    full_response = ""
    for token in provider.stream_completion(model_name, messages):
        chunk = "".join(token)
        full_response += chunk
        print(chunk, end="", flush=True)
    print()  # move to next line
    return full_response

def print_streaming_markdown(provider, model_name, messages) -> str:
    """
    Streams markdown content token by token and updates a live Markdown display.
    """
    full_response = ""
    # Live display will continuously update the rendered markdown.
    with Live(Markdown(""), refresh_per_second=10) as live:
        for token in provider.stream_completion(model_name, messages):
            chunk = "".join(token)
            full_response += chunk
            # Update the live markdown every iteration.
            live.update(Markdown(full_response))
    return full_response

def print_markdown(md_text: str):
    """
    Print multi-line text as markdown (code highlighting, etc.) using Rich.
    """
    markdown_obj = Markdown(md_text)
    console.print(markdown_obj)