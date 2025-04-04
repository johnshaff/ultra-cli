import os
import sys
import subprocess
import re
import shlex  # Added to handle special characters in URLs

def download_youtube_audio(url, output_path="audio") -> str:
    """
    Download a YouTube video's audio using yt-dlp and save it to the specified directory.
    
    Args:
        url (str): The YouTube video URL
        output_path (str): Directory to save the audio, defaults to 'aduio'
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Created directory: {output_path}")
      
        # Extract video ID from URL to use in filename
        video_id = None
        if "youtu.be" in url:
            video_id = url.split("/")[-1].split("?")[0]
        elif "youtube.com" in url:
            match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
            if match:
                video_id = match.group(1)
        
        if not video_id:
            video_id = "video"
        
        output_template = f"{output_path}/{video_id}.%(ext)s"
        
        # Download command with yt-dlp using a user-agent instead of cookies
        cmd = [
            "yt-dlp",
            "-f", "bestaudio",  # updated format specifier for a fallback
            "-o", output_template,
            "--extract-audio",  # Extract audio only
            "--audio-format", "mp3",  # Convert to MP3
            "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
            "--verbose",  # Verbose output
            url
        ]
        
        print(f"Downloading audio: {url}")
        subprocess.run(cmd, check=True)
        
        output_file = f"{output_path}/{video_id}.mp3"
        print(f"Download complete! Saved to: {output_file}")
        
        return video_id
        
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

if __name__ == "__main__":
    # Use the provided URL or take from command line arguments
    default_url = 'https://youtu.be/PpEIoBnQsKs?si=-brf8-42XVyk--VP'
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = default_url
    
    # Pass the URL directly without requiring quotes
    download_youtube_audio(url)