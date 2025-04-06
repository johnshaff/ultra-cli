import platform
import os
import sys
import nltk
import whisper
from pydub import AudioSegment
from nltk.tokenize.punkt import PunktSentenceTokenizer
from ultra.audio import download_youtube_audio
from ultra.providers import OpenAIProvider
from ultra.pdf import text_to_pdf
from ultra.config import get_api_key
import io
import logging
from ultra.logging_config import redirect_nested_logs

logger = logging.getLogger(__name__)



def transcribe_video(url: str) -> str:
    # ----------------------
    # Download Audio
    # ----------------------
    title = download_youtube_audio(url)
    
    # ----------------------
    # NLTK Setup
    # ----------------------
    nltk_data_dir = os.getcwd()
    nltk.data.path = [nltk_data_dir] + nltk.data.path
    redirect_nested_logs(nltk.download, 'punkt', download_dir=nltk_data_dir, quiet=True)
    tokenizer = PunktSentenceTokenizer()
    logger.info("Tokenizer loaded successfully!")
    
    # ----------------------
    # Load Whisper Model
    # ----------------------
    
    model = redirect_nested_logs(whisper.load_model, "base", "cpu", download_root="./models")

    
    # ----------------------
    # Transcribe Audio
    # ----------------------
    audio_file = f"audio/{title}.mp3"
    
    transcription = redirect_nested_logs(model.transcribe, audio_file, fp16=False, verbose=False)
    
    logger.info(f"Transcribing audio file: {audio_file}...")
   
    
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
        
    text_to_pdf(title)
    
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