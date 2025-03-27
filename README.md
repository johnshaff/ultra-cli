# Ultra CLI

`Ultra` is a command-line tool for interacting with various LLM (Large Language Model) providers. It supports multi-turn conversations, context management, and even compacting your conversation history using a cheaper model.

## Features
- Multiple provider support (OpenAI by default).
- Model selection and dynamic switching.
- Session-based context storage, with options to export the history.
- Lightweight terminal UI with color-coded prompts.
- Configurable ASCII art welcome screen.
- Basic streaming support for partial response updates.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-github-account/ultra-cli.git
    ```
2. Change into the directory and install:

    ```bash
    cd ultra-cli
    pip install .
    ```

3. Run with:

    ```bash
    ultra
    ```

Optionally set environment variables:
```bash
export OPENAI_API_KEY=your_openai_api_key