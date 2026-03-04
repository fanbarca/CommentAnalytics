# Top Themes by Volume using BERTopic or simple TF-IDF as fallback
try:
    from bertopic import BERTopic
    bertopic_available = True
except ImportError:
    bertopic_available = False
    
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def extract_themes_lda(documents: list, num_themes: int = 5) -> list:
    """
    Fallback: Extract topics using Latent Dirichlet Allocation
    """
    if not documents or len(documents) < num_themes:
         return []
         
    # Only keep valid strings
    docs = [d for d in documents if isinstance(d, str) and len(d.split()) > 3]
    if len(docs) < num_themes:
        return []

    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    try:
        tfidf = vectorizer.fit_transform(docs)
        lda = LatentDirichletAllocation(n_components=num_themes, random_state=42)
        lda.fit(tfidf)
        
        feature_names = vectorizer.get_feature_names_out()
        themes = []
        for topic_idx, topic in enumerate(lda.components_):
            top_features_ind = topic.argsort()[:-5 - 1:-1]
            top_features = [feature_names[i] for i in top_features_ind]
            themes.append({
                "theme_id": topic_idx,
                "keywords": top_features,
                "name": f"Theme {topic_idx + 1}: {', '.join(top_features[:3])}"
            })
        return themes
    except Exception as e:
        print(f"Error in LDA topic modeling: {e}")
        return []

def extract_themes_bertopic(documents: list) -> list:
    """
    Extract topics using BERTopic
    """
    if not documents or len(documents) < 10:
        return extract_themes_lda(documents)

    try:
        # A lightweight representation to avoid massive models
        topic_model = BERTopic(language="english", calculate_probabilities=False)
        topics, _ = topic_model.fit_transform(documents)
        
        topic_info = topic_model.get_topic_info()
        themes = []
        # skip -1 which is the outlier category
        for index, row in topic_info.iterrows():
            if row['Topic'] == -1:
                continue
            themes.append({
                "theme_id": row['Topic'],
                "name": row['Name'],
                "count": row['Count'],
                "keywords": [word for word, _ in topic_model.get_topic(row['Topic'])[:5]]
            })
            if len(themes) >= 5: # Limit to top 5 themes
                break
        return themes
    except Exception as e:
        print(f"Error in BERTopic modeling, falling back to LDA: {e}")
        return extract_themes_lda(documents)

def extract_themes(documents: list) -> list:
    if bertopic_available:
        return extract_themes_bertopic(documents)
    return extract_themes_lda(documents)
