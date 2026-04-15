"""Machine Learning prediction module for Amazon Bestsellers."""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score


class BookPredictor:
    """ML models for book predictions."""

    def __init__(self, df):
        self.df = df.copy()
        self.le_genre = LabelEncoder()
        self.scaler = StandardScaler()
        self.classifier = None
        self.regressor = None
        self.clf_metrics = {}
        self.reg_metrics = {}
        self._prepare_data()
        self._train_models()

    def _prepare_data(self):
        """Prepare features for ML models."""
        self.df['Genre_Encoded'] = self.le_genre.fit_transform(self.df['Genre'])

        # Bestseller label: top 25% by reviews = bestseller
        review_threshold = self.df['Reviews'].quantile(0.75)
        self.df['Is_Bestseller'] = (self.df['Reviews'] >= review_threshold).astype(int)

        self.feature_cols = ['Price', 'Year', 'Genre_Encoded']
        self.X = self.df[self.feature_cols].values
        self.X_scaled = self.scaler.fit_transform(self.X)

    def _train_models(self):
        """Train both classification and regression models."""
        # Classification: predict bestseller status
        y_cls = self.df['Is_Bestseller'].values
        X_train, X_test, y_train, y_test = train_test_split(
            self.X_scaled, y_cls, test_size=0.2, random_state=42
        )
        self.classifier = RandomForestClassifier(
            n_estimators=100, random_state=42, max_depth=10
        )
        self.classifier.fit(X_train, y_train)
        y_pred = self.classifier.predict(X_test)
        self.clf_metrics = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'feature_importance': dict(zip(
                ['Price', 'Year', 'Genre'],
                [float(x) for x in self.classifier.feature_importances_]
            ))
        }

        # Regression: predict user rating
        y_reg = self.df['User Rating'].values
        X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
            self.X_scaled, y_reg, test_size=0.2, random_state=42
        )
        self.regressor = GradientBoostingRegressor(
            n_estimators=100, random_state=42, max_depth=5, learning_rate=0.1
        )
        self.regressor.fit(X_train_r, y_train_r)
        y_pred_r = self.regressor.predict(X_test_r)
        self.reg_metrics = {
            'rmse': float(np.sqrt(mean_squared_error(y_test_r, y_pred_r))),
            'r2_score': float(r2_score(y_test_r, y_pred_r)),
            'feature_importance': dict(zip(
                ['Price', 'Year', 'Genre'],
                [float(x) for x in self.regressor.feature_importances_]
            ))
        }

    def predict_bestseller(self, price, year, genre):
        """Predict if a book will be a bestseller.

        Returns:
            dict: prediction result with probability
        """
        genre_encoded = self.le_genre.transform([genre])[0] if genre in self.le_genre.classes_ else 0
        features = self.scaler.transform([[price, year, genre_encoded]])
        prediction = self.classifier.predict(features)[0]
        probabilities = self.classifier.predict_proba(features)[0]

        return {
            'is_bestseller': bool(prediction),
            'probability': float(max(probabilities)),
            'confidence': 'High' if max(probabilities) > 0.7 else 'Medium' if max(probabilities) > 0.5 else 'Low'
        }

    def predict_rating(self, price, year, genre):
        """Predict user rating for a book.

        Returns:
            dict: predicted rating
        """
        genre_encoded = self.le_genre.transform([genre])[0] if genre in self.le_genre.classes_ else 0
        features = self.scaler.transform([[price, year, genre_encoded]])
        rating = self.regressor.predict(features)[0]
        rating = round(min(5.0, max(1.0, rating)), 2)

        return {
            'predicted_rating': rating,
            'rating_category': (
                'Outstanding' if rating >= 4.7 else
                'Excellent' if rating >= 4.5 else
                'Very Good' if rating >= 4.0 else 'Good'
            )
        }

    def get_model_info(self):
        """Get info about trained models."""
        return {
            'classification': {
                'model': 'Random Forest Classifier',
                'task': 'Predict if a book will be a bestseller (top 25% by reviews)',
                'metrics': self.clf_metrics
            },
            'regression': {
                'model': 'Gradient Boosting Regressor',
                'task': 'Predict user rating based on book features',
                'metrics': self.reg_metrics
            },
            'features_used': ['Price', 'Year', 'Genre'],
            'dataset_size': len(self.df)
        }
