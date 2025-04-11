import os
import glob
import logging

logger = logging.getLogger(__name__)

def open_video(video_id):
    videos_dir = "/Users/johnshaff/Documents/dev/video"
    pattern = os.path.join(videos_dir, f"{video_id}.*")
    matches = glob.glob(pattern)
    
    if not matches:
        logging.info(f"No video found for id: {video_id}")
        return
    
    # Use the first matching file; update if you need other behavior
    video_file = matches[0]
    
    try:
        result = os.system(f"open -na 'Microsoft Edge' --args --new-window '{video_file}'")
        if result != 0:
            logging.info(f"Failed to open the video file: {video_file}")
    except Exception as e:
        logging.info(f"An error occurred: {e}")

if __name__ == '__main__':
    # Call the function with the specific video file name
    open_video("Y__2UsC7T-I")