from fastapi import APIRouter, HTTPException
from typing import Optional
from .ingestion.youtube_api import get_video_metadata, get_video_comments, get_video_transcript
from .processing.cleaner import preprocess_text
from .modeling.vader_model import analyze_vader_sentiment
from .modeling.transformer import analyze_emotion
from .modeling.sarcasm import adjust_sentiment_for_sarcasm
from .modeling.absa import extract_aspect_sentiment
from .modeling.topic_modeling import extract_themes

api_router = APIRouter()

@api_router.get("/health")
def health_check():
    return {"status": "ok"}

@api_router.get("/analyze/{video_id}")
def analyze_video(video_id: str, max_comments: int = 100):
    """
    Main orchestration endpoint.
    1. Ingests video metadata, transcript, and comments.
    2. Runs text cleaning pipeline on comments.
    3. Runs models on comments (Sentiment, Emotion, Sarcasm).
    4. Extracts Aspects and Themes from comments.
    5. Returns aggregated dashboard data.
    """
    metadata = get_video_metadata(video_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Video not found or API limits exceeded.")
        
    transcript = get_video_transcript(video_id)
    comments_raw = get_video_comments(video_id, max_comments)
    
    if not comments_raw:
       return {
           "metadata": metadata,
           "message": "No comments found for this video",
           "data": None
       }

    processed_comments = []
    
    # Track overall statistics for the dashboard
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    emotion_counts = {}
    time_series = []
    all_clean_texts = []
    
    for c in comments_raw:
        clean_text = preprocess_text(c["text"])
        all_clean_texts.append(clean_text)
        
        # 1. Base Sentiment (VADER)
        base_sent = analyze_vader_sentiment(clean_text)
        
        # 2. Sarcasm Adjustment
        adj_sent = adjust_sentiment_for_sarcasm(c["text"], base_sent)
        
        # 3. Emotion Classification
        emotions = analyze_emotion(clean_text)
        # emotions format: [{'label': 'joy', 'score': 0.9}, ...]
        top_emotion = emotions[0]["label"] if emotions else "neutral"

        # Tally metrics
        sentiment_counts[adj_sent["label"]] += 1
        emotion_counts[top_emotion] = emotion_counts.get(top_emotion, 0) + 1
        
        time_series.append({
            "timestamp": c["published_at"],
            "compound": adj_sent["compound"]
        })
        
        processed_comments.append({
            "author": c["author"],
            "text": c["text"],
            "sentiment": adj_sent,
            "emotion": emotions,
            "likes": c["like_count"]
        })
        
    # Aggregate Aspects
    aspects = extract_aspect_sentiment(" ".join(all_clean_texts))
    
    # Aggregate Themes
    themes = extract_themes(all_clean_texts)
    
    # Sort time_series by timestamp
    time_series.sort(key=lambda x: x["timestamp"])

    return {
        "metadata": metadata,
        "transcript_preview": transcript[:500] + "..." if transcript else "",
        "dashboard": {
            "overall_sentiment": sentiment_counts,
            "top_emotions": sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "waterfall": time_series,
            "aspects": aspects,
            "themes": themes,
            "top_comments": sorted(processed_comments, key=lambda x: x["likes"], reverse=True)[:10]
        }
    }
