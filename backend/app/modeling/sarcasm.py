import emoji
import re
from .vader_model import analyze_vader_sentiment

# A basic heuristic:
# Often sarcasm is present when text sentiment is highly positive but the emoji is highly negative, or vice versa.
# Example: "Oh brilliant..." + 🙄 (rolling eyes: negative)
# Or "I just love waiting for 3 hours" + 😠 (angry)

# We can categorize common emojis by their sentiment valence 
NEGATIVE_EMOJIS = ["🙄", "😒", "😠", "😡", "🤬", "🤡", "💩", "💀", "🙃"]
POSITIVE_EMOJIS = ["😂", "😍", "🥰", "🥳", "🤩", "✨", "❤️", "🔥", "🙌"]

def extract_emojis(text: str) -> list:
    return [c for c in text if c in emoji.EMOJI_DATA]

def detect_sarcasm(text: str, text_sentiment_label: str) -> bool:
    """
    Detects potential sarcasm by evaluating conflict between text sentiment and emoji sentiment.
    """
    if not text:
        return False
        
    emojis_in_text = extract_emojis(text)
    if not emojis_in_text:
        # Harder to detect without emojis or deep learning model.
        # Fall back to heuristic: simple contradictions like "yeah right"
        if re.search(r'\b(yeah right|sure|oh great|just love)\b', text.lower()) and text_sentiment_label == "negative":
             # This is tricky without ML, but we'll flag simple keyword contradictions
             pass
        return False

    has_negative_emoji = any(e in NEGATIVE_EMOJIS for e in emojis_in_text)
    has_positive_emoji = any(e in POSITIVE_EMOJIS for e in emojis_in_text)

    # If text is positive but emoji is strictly negative -> Sarcastic
    if text_sentiment_label == "positive" and has_negative_emoji and not has_positive_emoji:
        return True
    
    # If text is negative but emoji is strictly positive (e.g., "This is the worst UI ever 😍")
    if text_sentiment_label == "negative" and has_positive_emoji and not has_negative_emoji:
        return True
        
    # An upside down face is almost always sarcastic
    if "🙃" in emojis_in_text:
        return True

    return False

def adjust_sentiment_for_sarcasm(text: str, base_sentiment: dict) -> dict:
    """
    If sarcasm is detected, we typically reverse the compound score and label.
    """
    is_sarcastic = detect_sarcasm(text, base_sentiment["label"])
    
    if is_sarcastic:
        # Flip the sentiment
        base_sentiment["compound"] = -base_sentiment["compound"]
        
        # Swap pos/neg
        temp = base_sentiment["pos"]
        base_sentiment["pos"] = base_sentiment["neg"]
        base_sentiment["neg"] = temp
        
        if base_sentiment["compound"] >= 0.05:
            base_sentiment["label"] = "positive"
        elif base_sentiment["compound"] <= -0.05:
            base_sentiment["label"] = "negative"
        else:
            base_sentiment["label"] = "neutral"
            
    base_sentiment["is_sarcastic"] = is_sarcastic
    return base_sentiment
