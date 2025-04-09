import platform
import os
import sys
import logging
from ultra.logging_config import redirect_nested_logs

# Only import non-heavy modules at the top level
from ultra.audio import download_youtube_audio
from ultra.config import get_api_key

logger = logging.getLogger(__name__)



def transcribe_video(url: str) -> str:
    # ----------------------
    # Download Audio
    # ----------------------
    title = download_youtube_audio(url)
    
    # Create transcript directory if it doesn't exist
    if not os.path.exists("transcript"):
        os.makedirs("transcript")
        logger.info("Created directory: transcript")
    
    # ----------------------
    # NLTK Setup - Lazy import
    # ----------------------
    logger.info("Loading NLP libraries...")
    import nltk
    from nltk.tokenize.punkt import PunktSentenceTokenizer
    
    nltk_data_dir = os.getcwd()
    nltk.data.path = [nltk_data_dir] + nltk.data.path
    redirect_nested_logs(nltk.download, 'punkt', download_dir=nltk_data_dir, quiet=True)
    tokenizer = PunktSentenceTokenizer()
    logger.info("Tokenizer loaded successfully!")
    
    # ----------------------
    # Load Whisper Model - Lazy import
    # ----------------------
    logger.info("Loading speech recognition model...")
    import whisper
    
    model = redirect_nested_logs(whisper.load_model, "base", "cpu", download_root="./models")

    # ----------------------
    # Transcribe Audio
    # ----------------------
    audio_file = f"audio/{title}.mp3"
    
    logger.info(f"Transcribing audio file: {audio_file}...")
    transcription = redirect_nested_logs(model.transcribe, audio_file, fp16=False, verbose=False)
    
    # ----------------------
    # Process Transcription
    # ----------------------
    logger.info("Formatting transcription...")
    
    with open(f"transcript/{title}-raw.txt", "w") as file:
        file.write(transcription["text"].strip())
    
    with open(f"transcript/{title}-raw.txt", "r") as input_file:
        text = input_file.read()
    
    sentences = tokenizer.tokenize(text)
    output_text = "\n".join(sentences)
    
    with open(f"transcript/{title}-sentences.txt", "w") as output_file:
        output_file.write(output_text)
    
    # Lazy import PDF module
    logger.info("Converting to PDF...")
    from ultra.pdf import text_to_pdf
    text_to_pdf(title)
    
    # Lazy import OpenAI provider
    logger.info("Formatting with AI...")
    from ultra.providers import OpenAIProvider
    chatgpt = OpenAIProvider(get_api_key("openai"))
    formatted_text = chatgpt.format_transcription(f"transcript/{title}-final.pdf")
    
    with open(f"transcript/{title}-final.txt", "w") as output_file:
        output_file.write(formatted_text)
    
    os.remove(f"transcript/{title}-raw.txt")
    os.remove(f"transcript/{title}-sentences.txt")
    os.remove(f"transcript/{title}-final.pdf")
    
    logger.info(f"Transcription complete! Saved to transcript/{title}-final.txt")
    
    return url
    
    '''
    if platform.system() == "Darwin":
        os.system(f"open transcript/{title}-final.txt")
    elif platform.system() == "Windows":
        os.startfile(f"transcript/{title}-final.txt")
    else:
    # Assume Linux
        os.system(f"xdg-open transcript/{title}-final.txt")
    '''
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <youtube_url>")
        sys.exit(1)
    url = sys.argv[1]
    transcribe_video(url)