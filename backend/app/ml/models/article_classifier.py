from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from app.ml.features.text_features import TextFeatureExtractor
from typing import List, Dict, Any, Optional
import numpy as np
import joblib
from pathlib import Path

class ArticleClassifier:
    def __init__(self, model_dir: Optional[Path] = None):
        self.text_features = TextFeatureExtractor()
        self.category_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.priority_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )
        self.category_encoder = LabelEncoder()
        self.is_fitted = False
        self.model_dir = model_dir or Path(__file__).parent / "saved_models"
        self.model_dir.mkdir(parents=True, exist_ok=True)
    
    def fit(self, texts: List[str], categories: List[str], priorities: List[str]) -> None:
        """Train the classifiers"""
        # Extract text features
        features = self.text_features.extract_features(texts, fit=True)
        
        # Fit category classifier
        encoded_categories = self.category_encoder.fit_transform(categories)
        self.category_classifier.fit(features, encoded_categories)
        
        # Fit priority classifier
        self.priority_classifier.fit(features, [1 if p == "High" else 0 for p in priorities])
        
        self.is_fitted = True
    
    def predict(self, text: str) -> Dict[str, Any]:
        """Predict category and priority for a new article"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        # Extract features
        features = self.text_features.extract_features([text])
        
        # Predict category
        category_proba = self.category_classifier.predict_proba(features)[0]
        category_idx = np.argmax(category_proba)
        category = self.category_encoder.inverse_transform([category_idx])[0]
        
        # Predict priority
        priority_proba = self.priority_classifier.predict_proba(features)[0]
        priority = "High" if priority_proba[1] > 0.7 else "Low"
        
        # Get key terms
        key_terms = self.text_features.get_top_terms(text)
        
        return {
            "category": category,
            "category_confidence": float(category_proba[category_idx]),
            "priority": priority,
            "priority_confidence": float(priority_proba[1]),
            "key_terms": key_terms
        }
    
    def save(self) -> None:
        """Save the model to disk"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        joblib.dump(self.category_classifier, self.model_dir / "category_classifier.pkl")
        joblib.dump(self.priority_classifier, self.model_dir / "priority_classifier.pkl")
        joblib.dump(self.category_encoder, self.model_dir / "category_encoder.pkl")
        joblib.dump(self.text_features.vectorizer, self.model_dir / "vectorizer.pkl")
    
    def load(self) -> None:
        """Load the model from disk"""
        try:
            self.category_classifier = joblib.load(self.model_dir / "category_classifier.pkl")
            self.priority_classifier = joblib.load(self.model_dir / "priority_classifier.pkl")
            self.category_encoder = joblib.load(self.model_dir / "category_encoder.pkl")
            self.text_features.vectorizer = joblib.load(self.model_dir / "vectorizer.pkl")
            self.text_features.is_fitted = True
            self.is_fitted = True
        except FileNotFoundError:
            raise ValueError("No saved model found. Train the model first.") 