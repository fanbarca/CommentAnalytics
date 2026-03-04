import spacy
from .vader_model import analyze_vader_sentiment

# Load spaCy instance
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

def extract_aspect_sentiment(text: str, aspects: list = None) -> dict:
    """
    Aspect-Based Sentiment Analysis.
    Given a list of aspects (e.g., ["quality", "audio", "video", "content"]),
    this extracts sentiments strictly tied to the phrase containing the aspect.
    """
    if nlp is None or not text:
        return {}

    if aspects is None:
        # Predefined fallback aspects usually relevant for YouTube
        aspects = ["quality", "audio", "video", "content", "host", "editing", "music", "grammar", "engagement"]
        
    doc = nlp(text)
    aspect_sentiments = {}

    for sentence in doc.sents:
        sent_str = sentence.text.lower()
        for aspect in aspects:
            if aspect in sent_str:
                # Calculate sentiment of just the sentence containing the aspect
                sentiment = analyze_vader_sentiment(sentence.text)
                
                if aspect not in aspect_sentiments:
                    aspect_sentiments[aspect] = []
                    
                aspect_sentiments[aspect].append({
                    "text": sentence.text,
                    "sentiment": sentiment["label"],
                    "compound": sentiment["compound"]
                })
                
    # Aggregate sentiment for each aspect
    aggregated = {}
    for aspect, records in aspect_sentiments.items():
        avg_compound = sum(r["compound"] for r in records) / len(records)
        if avg_compound >= 0.05:
            label = "positive"
        elif avg_compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
            
        aggregated[aspect] = {
            "compound": avg_compound,
            "label": label,
            "mentions": len(records),
            "quotes": [r["text"] for r in records]
        }
        
    return aggregated
