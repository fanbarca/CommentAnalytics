from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from app.core.config import settings

def get_youtube_client():
    if not settings.YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY is not set")
    return build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

def get_video_metadata(video_id: str) -> dict:
    try:
        youtube = get_youtube_client()
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        
        if not response.get("items"):
            return None
            
        item = response["items"][0]
        return {
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "description": item["snippet"]["description"],
            "published_at": item["snippet"]["publishedAt"],
            "view_count": int(item["statistics"].get("viewCount", 0)),
            "like_count": int(item["statistics"].get("likeCount", 0)),
            "comment_count": int(item["statistics"].get("commentCount", 0)),
        }
    except Exception as e:
        print(f"Error fetching metadata for {video_id}: {str(e)}")
        return None

def get_video_comments(video_id: str, max_results: int = 100) -> list:
    comments = []
    try:
        youtube = get_youtube_client()
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_results, 100),
            textFormat="plainText"
        )
        
        while request and len(comments) < max_results:
            response = request.execute()
            
            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "id": item["id"],
                    "author": comment["authorDisplayName"],
                    "text": comment["textDisplay"],
                    "like_count": comment["likeCount"],
                    "published_at": comment["publishedAt"],
                    "updated_at": comment["updatedAt"]
                })
                
            if "nextPageToken" in response and len(comments) < max_results:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    pageToken=response["nextPageToken"],
                    maxResults=min(100, max_results - len(comments)),
                    textFormat="plainText"
                )
            else:
                break
                
    except HttpError as e:
        print(f"YouTube API Error fetching comments for {video_id}: {e}")
    except Exception as e:
         print(f"Error fetching comments for {video_id}: {str(e)}")
         
    return comments

def get_video_transcript(video_id: str) -> str:
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript_list)
        return text_formatted
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return ""
