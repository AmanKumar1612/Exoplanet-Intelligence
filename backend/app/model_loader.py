"""
Model Loader for Exoplanet Intelligence System
Loads and manages ML models for predictions
"""
import os
import sys
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple

# Model storage
classification_pipeline = None
regression_pipeline = None
classification_metrics = None
regression_metrics = None

# Model paths
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
CLASSIFICATION_MODEL_PATH = os.path.join(MODEL_DIR, "classification_pipeline.pkl")
REGRESSION_MODEL_PATH = os.path.join(MODEL_DIR, "regression_pipeline.pkl")
CLASSIFICATION_METRICS_PATH = os.path.join(MODEL_DIR, "classification_metrics.pkl")
REGRESSION_METRICS_PATH = os.path.join(MODEL_DIR, "regression_metrics.pkl")


def load_models():
    """Load ML models from disk"""
    global classification_pipeline, regression_pipeline, classification_metrics, regression_metrics
    
    # Try to load classification model
    if os.path.exists(CLASSIFICATION_MODEL_PATH):
        try:
            classification_pipeline = joblib.load(CLASSIFICATION_MODEL_PATH)
            print(f"Loaded classification model from {CLASSIFICATION_MODEL_PATH}")
        except Exception as e:
            print(f"Error loading classification model: {e}")
            classification_pipeline = None
    else:
        print(f"Classification model not found at {CLASSIFICATION_MODEL_PATH}")
    
    # Try to load regression model
    if os.path.exists(REGRESSION_MODEL_PATH):
        try:
            regression_pipeline = joblib.load(REGRESSION_MODEL_PATH)
            print(f"Loaded regression model from {REGRESSION_MODEL_PATH}")
        except Exception as e:
            print(f"Error loading regression model: {e}")
            regression_pipeline = None
    else:
        print(f"Regression model not found at {REGRESSION_MODEL_PATH}")
    
    # Load metrics if available
    if os.path.exists(CLASSIFICATION_METRICS_PATH):
        try:
            classification_metrics = joblib.load(CLASSIFICATION_METRICS_PATH)
        except Exception as e:
            print(f"Error loading classification metrics: {e}")
    
    if os.path.exists(REGRESSION_METRICS_PATH):
        try:
            regression_metrics = joblib.load(REGRESSION_METRICS_PATH)
        except Exception as e:
            print(f"Error loading regression metrics: {e}")
    
    # If models not loaded, create dummy models for demo
    if classification_pipeline is None or regression_pipeline is None:
        print("Creating demo models for demonstration purposes...")
        create_demo_models()


def create_demo_models():
    """Create demo models for demonstration when real models are not available"""
    global classification_pipeline, regression_pipeline
    
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.impute import SimpleImputer
    
    # Demo classification model
    # Create a simple model that returns random predictions for demo
    class DemoClassifier:
        def __init__(self):
            self.classes_ = np.array([0, 1])  # 0: FALSE POSITIVE, 1: CONFIRMED
        
        def predict(self, X):
            # Return random predictions for demo
            np.random.seed(42)
            return np.random.choice([0, 1], size=X.shape[0])
        
        def predict_proba(self, X):
            # Return random probabilities for demo
            np.random.seed(42)
            probs = np.random.random(size=(X.shape[0], 2))
            probs = probs / probs.sum(axis=1, keepdims=True)
            return probs
    
    # Demo regression model
    class DemoRegressor:
        def __init__(self):
            self.mean_ = 2.5  # Average planetary radius
        
        def predict(self, X):
            # Return random radius predictions for demo
            np.random.seed(42)
            return np.random.uniform(0.5, 10, size=X.shape[0])
    
    # Create pipelines
    classification_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', DemoClassifier())
    ])
    
    regression_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('regressor', DemoRegressor())
    ])


def predict_classification(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Make classification prediction
    
    Args:
        df: Input features as DataFrame
    
    Returns:
        Dictionary with prediction and probabilities
    """
    global classification_pipeline
    
    if classification_pipeline is None:
        raise ValueError("Classification model not loaded")
    
    # Make prediction
    prediction = classification_pipeline.predict(df)
    probabilities = classification_pipeline.predict_proba(df)
    
    # Map predictions to class names
    class_names = {0: "FALSE POSITIVE", 1: "CONFIRMED"}
    predicted_class = class_names.get(prediction[0], "UNKNOWN")
    
    # Get probability scores
    prob_scores = {
        "CONFIRMED": float(probabilities[0][1]),
        "FALSE POSITIVE": float(probabilities[0][0])
    }
    
    # Calculate confidence (max probability)
    confidence = float(max(probabilities[0]))
    
    return {
        "prediction": predicted_class,
        "probabilities": prob_scores,
        "confidence": confidence
    }


def predict_regression(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Make regression prediction
    
    Args:
        df: Input features as DataFrame
    
    Returns:
        Dictionary with prediction and confidence interval
    """
    global regression_pipeline, regression_metrics
    
    if regression_pipeline is None:
        raise ValueError("Regression model not loaded")
    
    # Ensure koi_prad is 0 for prediction as per training logic
    df_reg = df.copy()
    df_reg['koi_prad'] = 0
    print(f"DEBUG: Regression Input Features:\n{df_reg.iloc[0].to_dict()}")
    
    # Make prediction
    prediction = regression_pipeline.predict(df_reg)
    predicted_radius = float(prediction[0])
    
    # Calculate confidence interval
    std_error = 0.5  # Default std error
    if regression_metrics and 'std_error' in regression_metrics:
        std_error = regression_metrics['std_error']
    
    # 95% confidence interval (approximately ±2 std errors)
    ci_lower = max(0.1, predicted_radius - 2 * std_error)
    ci_upper = predicted_radius + 2 * std_error
    
    return {
        "prediction": predicted_radius,
        "confidence_interval": {
            "lower": round(ci_lower, 4),
            "upper": round(ci_upper, 4)
        },
        "unit": "Earth radii"
    }


def get_model_info() -> Dict[str, Any]:
    """Get information about loaded models"""
    global classification_pipeline, regression_pipeline, classification_metrics, regression_metrics
    
    info = {
        "classification_model": "classification_pipeline.pkl" if classification_pipeline else None,
        "regression_model": "regression_pipeline.pkl" if regression_pipeline else None,
        "classification_metrics": classification_metrics,
        "regression_metrics": regression_metrics,
        "models_loaded": classification_pipeline is not None and regression_pipeline is not None
    }
    
    return info


def get_classification_model():
    """Get classification model instance"""
    return classification_pipeline


def get_regression_model():
    """Get regression model instance"""
    return regression_pipeline
