import requests
import argparse
import os
import sys

def post_video_to_facebook(page_id, access_token, video_path, description="", title=""):
    """
    Posts a video to a Facebook Page using the simple (non-resumable) upload method.
    Suitable for smaller video files.
    """
    url = f"https://graph-video.facebook.com/v20.0/{page_id}/videos"
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return None

    files = {
        'source': open(video_path, 'rb')
    }
    
    data = {
        'description': description,
        'title': title,
        'access_token': access_token
    }
    
    print(f"Uploading video to Facebook Page {page_id}...")
    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        result = response.json()
        print(f"Successfully posted video! ID: {result.get('id')}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Failed to post video: {e}")
        if response is not None:
            print(f"Response: {response.text}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a video to a Facebook Page.")
    parser.add_argument("video_path", help="Path to the video file to upload.")
    parser.add_argument("--page-id", required=True, help="Facebook Page ID.")
    parser.add_argument("--token", required=True, help="Facebook Page Access Token.")
    parser.add_argument("--description", default="", help="Description for the video post.")
    parser.add_argument("--title", default="", help="Title for the video.")

    args = parser.parse_args()

    post_video_to_facebook(
        args.page_id, 
        args.token, 
        args.video_path, 
        args.description, 
        args.title
    )
