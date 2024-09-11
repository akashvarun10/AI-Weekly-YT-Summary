# services/youtube_service.py
from googleapiclient.discovery import build
from config.settings import settings
import logging
from fastapi import HTTPException  # Add this import

youtube = build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)

def get_channel_id(channel_name: str) -> str:
    try:
        request = youtube.search().list(
            q=channel_name,
            type="channel",
            part="id",
            maxResults=1
        )
        response = request.execute()
        if response["items"]:
            return response["items"][0]["id"]["channelId"]
        return None
    except Exception as e:
        logging.error(f"Error getting channel ID for {channel_name}: {e}")
        return None

def get_latest_video_url(channel_id: str) -> str:
    try:
        request = youtube.search().list(
            channelId=channel_id,
            type="video",
            part="id",
            order="date",
            maxResults=1
        )
        response = request.execute()
        if response["items"]:
            return f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"
        return None
    except Exception as e:
        logging.error(f"Error getting latest video URL for channel {channel_id}: {e}")
        return None

# def fetch_channels(query: str):
#     try:
#         search_response = youtube.search().list(q=query, type="channel", part="snippet", maxResults=5).execute()
#         channels = [
#             {"name": item["snippet"]["title"], "id": item["snippet"]["channelId"]}
#             for item in search_response["items"]
#         ]
#         return channels
#     except Exception as e:
#         logging.error(f"Error in fetch_channels: {e}")
#         raise

def fetch_channels(query: str):
    try:
        request = youtube.search().list(
            q=query,
            type="channel",
            part="snippet",
            maxResults=5
        )
        response = request.execute()
        channels = [
            {
                "name": item["snippet"]["title"],
                "id": item["snippet"]["channelId"],
                "profilePicture": item["snippet"]["thumbnails"]["default"]["url"]  # Add profile picture URL
            }
            for item in response["items"]
        ]
        return channels
    except Exception as e:
        logging.error(f"Error in fetch_channels: {e}")
        raise HTTPException(status_code=500, detail="Error fetching channels")

