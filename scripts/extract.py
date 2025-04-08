import os
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")

# Set up the YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)

# Call the API to get trending videos in the US
request = youtube.videos().list(
    part="snippet,statistics",
    chart="mostPopular",
    regionCode="US",
    maxResults=10
)
response = request.execute()

# Process the data into a pandas DataFrame
videos = []
for item in response["items"]:
    video = {
        "title": item["snippet"]["title"],
        "channel": item["snippet"]["channelTitle"],
        "category_id": item["snippet"]["categoryId"],
        "publish_time": item["snippet"]["publishedAt"],
        "views": item["statistics"].get("viewCount", 0),
        "likes": item["statistics"].get("likeCount", 0),
        "comments": item["statistics"].get("commentCount", 0),
    }
    videos.append(video)

df = pd.DataFrame(videos)

# Save to CSV in the data/ folder
output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(output_dir, exist_ok=True)  # creates the folder if it doesn't exist

output_path = os.path.join(output_dir, "trending_videos.csv")
df.to_csv(output_path, index=False)

print("✅ Trending videos saved to", output_path)
