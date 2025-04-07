import os
import requests
import os.path

def download_thumbnail(url: str, video_id: str) -> None:
    output_dir = "images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract the file extension from the URL (e.g., '.jpg')
    ext = os.path.splitext(url.split("/")[-1])[1]
    filename = f"{video_id}{ext}"
    file_path = os.path.join(output_dir, filename)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        print(f"Thumbnail downloaded successfully to {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading thumbnail: {e}")

# Example usage:
if __name__ == "__main__":
    url = "https://i.ytimg.com/vi/qlyDnbNBiXE/maxresdefault.jpg"
    video_id = "qlyDnbNBiXE"
    download_thumbnail(url, video_id)