from transformers import pipeline

# We use a lightweight roberta model fine-tuned on GoEmotions.
# GoEmotions has 27 categories + neutral.
# We will initialize this lazily so it doesn't block app startup, or we could load it on startup depending on deployment.
emotion_classifier = None

def get_emotion_classifier():
    global emotion_classifier
    if emotion_classifier is None:
        try:
            # SamLowe is a good default for go_emotions on HuggingFace
            emotion_classifier = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=3)
        except Exception as e:
            print(f"Error loading emotion classifier: {e}")
            return None
    return emotion_classifier

def analyze_emotion(text: str) -> list:
    """
    Returns the top 3 emotions and their scores.
    """
    if not text or not isinstance(text, str):
        return []
    
    classifier = get_emotion_classifier()
    if not classifier:
        return []

    try:
        # The output is [[{'label': 'approval', 'score': 0.8}, ...]] since top_k=3
        results = classifier(text)
        return results[0]
    except Exception as e:
        print(f"Error during emotion classification: {e}")
        return []
