import re
import emoji
import spacy
from typing import List

# Load spaCy English model. Since we might parse large amounts of text, we will load it once.
# To avoid the dependency failure during installation, we might need a fallback or ensure spacy download is run.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # We will need to install this model in a separate command: python -m spacy download en_core_web_sm
    nlp = None

# A basic dictionary for slang normalization
SLANG_DICT = {
    "gud": "good",
    "idk": "i do not know",
    "smh": "shaking my head",
    "fyi": "for your information",
    "imo": "in my opinion",
    "imho": "in my humble opinion",
    "tbh": "to be honest",
    "lol": "laughing out loud",
    "lmao": "laughing my ass off",
    "omg": "oh my god",
    "wtf": "what the fuck",
    "rn": "right now",
    "afaik": "as far as I know",
    "brb": "be right back",
    "jk": "just kidding",
    "np": "no problem",
    "thx": "thanks",
    "ty": "thank you",
    "b/c": "because",
    "bc": "because",
    "pls": "please",
    "plz": "please",
}

def clean_noise(text: str) -> str:
    """Removes URLs, HTML tags, and user mentions."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    # Remove user mentions (@username)
    text = re.sub(r'@\w+', '', text)
    return text

def normalize_slang(text: str) -> str:
    """Translates informal internet vernacular to formal equivalents."""
    words = text.split()
    normalized_words = [SLANG_DICT.get(word.lower(), word) for word in words]
    return " ".join(normalized_words)

def handle_emojis(text: str) -> str:
    """Translates emojis into their textual representations."""
    # We use emoji.demojize which translates 😭 to :loudly_crying_face:
    # We replace colons and underscores to make it plain text "loudly crying face"
    demojized = emoji.demojize(text)
    # Convert :loudly_crying_face: to " loudly crying face "
    demojized = re.sub(r':(.*?):', lambda x: f" {x.group(1).replace('_', ' ')} ", demojized)
    # clean extra spaces
    demojized = re.sub(r'\s+', ' ', demojized).strip()
    return demojized

def handle_punctuation(text: str) -> str:
    """
    Remove non-repeated punctuation to reduce noise.
    Keep repeated punctuation like !! or ... as it might indicate emphasis.
    """
    # Replace single punctuations with space, keep consecutive punctuations (length >= 2)
    # This is a bit tricky with regex, simpler is just removing isolated punctuations.
    # We'll preserve ?, !, and . as they are important for sentence boundaries or VADER sentiment.
    # Just remove generic noise like (, ), [, ], {, }, ~, etc.
    text = re.sub(r'[()\[\]{}~\\|/]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def handle_negation(text: str) -> str:
    """
    Basic rule-based flipping or dependency parsing scope identification.
    Because VADER handles "not good" naturally, we might only need this for custom models
    or we just rely on VADER/Transformer internally for negation.
    But to fulfill the requirement, we use spacy to attach negation prefix explicitly (e.g., NOT_happy).
    """
    if nlp is None:
        return text # Fallback if spacy model is missing

    doc = nlp(text)
    tokens_with_negation = []
    
    for token in doc:
        # Check if the token's child is a negation
        is_negated = any(child.dep_ == "neg" for child in token.children)
        
        if is_negated:
            tokens_with_negation.append(f"NOT_{token.text}")
        else:
            tokens_with_negation.append(token.text)
            
    # For now, we will return the original text if we are using transformers,
    # as transformers prefer native text over "NOT_happy"
    # But for rule based or Bag of Words, "NOT_" prefixing is useful.
    # Return the doc text for VADER and Transformers natively, 
    # but the explicit negation string can be used if requested.
    return " ".join(tokens_with_negation)

def preprocess_text(text: str, apply_negation_prefix: bool = False) -> str:
    """Full preprocessing pipeline."""
    if not isinstance(text, str):
         return ""
         
    text = clean_noise(text)
    text = handle_emojis(text)
    text = handle_punctuation(text)
    text = normalize_slang(text)
    
    if apply_negation_prefix:
        text = handle_negation(text)
        
    return text.strip()
