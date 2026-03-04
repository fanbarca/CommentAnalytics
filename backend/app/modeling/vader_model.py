from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_vader_sentiment(text: str) -> dict:
    """
    Returns Positive, Negative, Neutral, and Compound scores.
    VADER is attuned to social media text and handles punctuation emphasis well.
    """
    if not text or not isinstance(text, str):
        return {"pos": 0.0, "neu": 1.0, "neg": 0.0, "compound": 0.0, "label": "neutral"}
        
    scores = analyzer.polarity_scores(text)
    
    # Classify based on compound score
    compound = scores['compound']
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
        
    scores["label"] = label
    return scores
