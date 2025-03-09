from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Any
import numpy as np
import re

class TextFeatureExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        self.is_fitted = False
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove special characters and digits
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def extract_features(self, texts: List[str], fit: bool = False) -> np.ndarray:
        """Extract TF-IDF features from texts"""
        cleaned_texts = [self.clean_text(text) for text in texts]
        
        if fit:
            features = self.vectorizer.fit_transform(cleaned_texts)
            self.is_fitted = True
        else:
            if not self.is_fitted:
                raise ValueError("Vectorizer must be fitted before transform")
            features = self.vectorizer.transform(cleaned_texts)
        
        return features.toarray()
    
    def get_feature_names(self) -> List[str]:
        """Get feature names (vocabulary)"""
        if not self.is_fitted:
            raise ValueError("Vectorizer must be fitted before getting feature names")
        return self.vectorizer.get_feature_names_out()
    
    def get_top_terms(self, text: str, n: int = 5) -> List[Dict[str, Any]]:
        """Get top n terms with their TF-IDF scores for a given text"""
        if not self.is_fitted:
            raise ValueError("Vectorizer must be fitted before getting top terms")
        
        # Extract features for the text
        features = self.extract_features([text])
        
        # Get feature names
        feature_names = self.get_feature_names()
        
        # Get indices of top n scores
        top_indices = np.argsort(features[0])[-n:][::-1]
        
        return [
            {
                "term": feature_names[idx],
                "score": float(features[0][idx])
            }
            for idx in top_indices
        ] 