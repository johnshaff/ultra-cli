import os
import subprocess
import json
import shlex
#from thumbnail import download_thumbnail  # Import the thumbnail downloader



def download_video_info(url: str) -> str:
    # Build the command using the user-agent (no cookies used)
    command = [
        "yt-dlp",
        "--skip-download",
        "--print-json",
        "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        url,
    ]
    
    print("Running command:")
    print(" ".join(shlex.quote(arg) for arg in command))
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("yt-dlp failed:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return
    
    info_str = result.stdout.strip()
    
    try:
        info_dict = json.loads(info_str)
    except json.JSONDecodeError:
        print("Failed to parse JSON output.")
        return

    # Use video id for naming
    video_id = info_dict.get('id', 'unknown')
    video_duration = info_dict.get('duration', 'Unknown Duration')
    video_title = info_dict.get('title', 'Unknown Title')
    video_description = info_dict.get('description', 'No Description')
    video_thumbnail = info_dict.get('thumbnail', 'No Thumbnail')
    video_upload_date = info_dict.get('upload_date', 'Unknown Upload Date')
    video_view_count = info_dict.get('view_count', 'Unknown View Count')
    video_like_count = info_dict.get('like_count', 'Unknown Like Count')
    video_dislike_count = info_dict.get('dislike_count', 'Unknown Dislike Count')
    video_comment_count = info_dict.get('comment_count', 'Unknown Comment Count')
    video_uploader = info_dict.get('uploader', 'Unknown Uploader')
    video_uploader_id = info_dict.get('uploader_id', 'Unknown Uploader ID')
    video_categories = ', '.join(info_dict.get('categories', []))
    video_tags = ', '.join(info_dict.get('tags', []))

    # Create custom dictionary with extracted data
    custom_dict = {
        "id": video_id,
        "duration": video_duration,
        "title": video_title,
        "description": video_description,
        "thumbnail": video_thumbnail,
        "upload_date": video_upload_date,
        "view_count": video_view_count,
        "like_count": video_like_count,
        "dislike_count": video_dislike_count,
        "comment_count": video_comment_count,
        "uploader": video_uploader,
        "uploader_id": video_uploader_id,
        "categories": video_categories,
        "tags": video_tags,
    }
    
    # Save the full JSON data
    '''
    full_json_filename = f"json/{video_id}.json"
    with open(full_json_filename, "w") as json_file:
        json.dump(info_dict, json_file, indent=4)
    '''
    
    # Save the custom JSON data
    custom_json_filename = f"json/custom-{video_id}.json"
    with open(custom_json_filename, "w") as custom_file:
        json.dump(custom_dict, custom_file, indent=4)
    
   
    print(f"Custom JSON data saved to: {custom_json_filename}")
    
    # Download the thumbnail using the imported download_thumbnail function
    # download_thumbnail(video_thumbnail, video_id)
    
    process_custom_json(custom_json_filename)
    return custom_json_filename
    
    
def numbers_to_strings(data):
    """
    Converts numerical view_count, like_count, and comment_count fields into formatted strings with commas.
    """
    for key in ["view_count", "like_count", "comment_count"]:
        value = data.get(key)
        if isinstance(value, (int, float)):
            data[key] = "{:,}".format(value)
    return data


def dates_to_strings(data):
    """
    Converts the upload_date (YYYYMMDD) string into a formatted date string like 'April 2, 2025'.
    """
    from datetime import datetime

    date_str = data.get("upload_date")
    try:
        # Assume the raw format is YYYYMMDD
        d = datetime.strptime(date_str, "%Y%m%d")
        # Format the date. On macOS, %-d works to remove any leading zeros.
        data["upload_date"] = d.strftime("%B %-d, %Y")
    except (ValueError, TypeError):
        # in case the date is not in expected format, leave it unchanged
        pass
    return data


def numbers_to_time(data):
    """
    Converts the duration (in seconds) to a formatted time string:
    HH:MM:SS if one hour or more, otherwise MM:SS.
    """
    seconds = data.get("duration")
    if isinstance(seconds, (int, float)):
        seconds = int(seconds)
        if seconds >= 3600:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            data["duration"] = f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            minutes = seconds // 60
            secs = seconds % 60
            data["duration"] = f"{minutes:02d}:{secs:02d}"
    return data


def process_custom_json(filename):
    """
    Loads the custom JSON file, applies the three functions to update its fields,
    and then writes the changes back to the same file.
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except Exception as e:
        print(f"Failed to load JSON file: {e}")
        return

    # Apply the transformations
    data = numbers_to_strings(data)
    data = dates_to_strings(data)
    data = numbers_to_time(data)

    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Processed JSON data saved to: {filename}")
    except Exception as e:
        print(f"Failed to write JSON file: {e}")



if __name__ == "__main__":
    # Existing interactive processing for yt-dlp video info
    video_url = input("Enter the video URL: ")
    download_video_info(video_url)

