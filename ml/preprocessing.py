"""
Data preprocessing pipeline for Exoplanet Intelligence System
"""
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
import joblib
import os


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Custom transformer for feature engineering"""
    
    def __init__(self):
        self.feature_names_ = []
        
    def fit(self, X, y=None):
        # Store feature names during fit
        self.feature_names_ = X.columns.tolist()
        return self
    
    def transform(self, X):
        """Apply feature engineering transformations"""
        X = X.copy()
        
        # Create derived features
        if 'koi_prad' in X.columns and 'koi_srad' in X.columns:
            # Planet-to-star radius ratio
            X['radius_ratio'] = X['koi_prad'] / (X['koi_srad'] + 0.001)
            
        if 'koi_period' in X.columns and 'koi_duration' in X.columns:
            # Transit duration to period ratio
            X['duration_ratio'] = X['koi_duration'] / (X['koi_period'] + 0.001)
            
        if 'koi_depth' in X.columns and 'koi_prad' in X.columns:
            # Transit depth per planetary radius
            X['depth_per_radius'] = X['koi_depth'] / (X['koi_prad'] + 0.001)
            
        if 'koi_srad' in X.columns and 'koi_steff' in X.columns:
            # Luminosity approximation (simplified)
            X['lum_approx'] = (X['koi_srad'] ** 2) * ((X['koi_steff'] / 5778) ** 4)
            
        if 'koi_impact' in X.columns and 'koi_duration' in X.columns:
            # Impact parameter-duration interaction
            X['impact_duration'] = X['koi_impact'] * X['koi_duration']
            
        if 'koi_model_snr' in X.columns and 'koi_depth' in X.columns:
            # Signal-to-noise per depth
            X['snr_per_depth'] = X['koi_model_snr'] / (np.sqrt(X['koi_depth']) + 0.001)
            
        return X
    
    def get_feature_names(self):
        return self.feature_names_


class SelectiveImputer(BaseEstimator, TransformerMixin):
    """Imputer that only imputes numeric columns"""
    
    def __init__(self, strategy='median'):
        self.strategy = strategy
        self.imputer = SimpleImputer(strategy=strategy)
        self.numeric_columns_ = []
        
    def fit(self, X, y=None):
        # Identify numeric columns
        self.numeric_columns_ = X.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(self.numeric_columns_) > 0:
            self.imputer.fit(X[self.numeric_columns_])
        return self
    
    def transform(self, X):
        X = X.copy()
        
        if len(self.numeric_columns_) > 0:
            X[self.numeric_columns_] = self.imputer.transform(X[self.numeric_columns_])
            
        return X


class ColumnSelector(BaseEstimator, TransformerMixin):
    """Select only the specified columns"""
    
    def __init__(self, columns=None):
        self.columns = columns
        
    def fit(self, X, y=None):
        if self.columns is None:
            self.columns_ = X.columns.tolist()
        else:
            self.columns_ = [col for col in self.columns if col in X.columns]
        return self
    
    def transform(self, X):
        return X[self.columns_]


def load_and_preprocess_data(filepath):
    """Load and preprocess the KOI dataset"""
    
    # Load data
    df = pd.read_csv(filepath)
    
    # Drop identifier columns
    id_columns = ['koi_name', 'koi_pdisposition', 'koi_tce_delivname', 
                  'koi_vet_stat', 'koi_vet_date', 'kepler_name']
    df = df.drop(columns=[col for col in id_columns if col in df.columns], errors='ignore')
    
    # Drop rows with missing target
    df = df.dropna(subset=['koi_disposition'])
    
    # Create binary target for classification (CONFIRMED vs FALSE POSITIVE)
    # Exclude CANDIDATE for binary classification
    df_classification = df[df['koi_disposition'].isin(['CONFIRMED', 'FALSE POSITIVE'])].copy()
    
    return df, df_classification


def get_feature_columns(df):
    """Get feature columns for modeling (exclude target and ID columns)"""
    
    # Columns to exclude
    exclude_columns = [
        'koi_disposition',  # Target for classification
        'koi_prad',         # Target for regression
        'koi_name',
        'kepler_name',
        'koi_pdisposition',
        'koi_tce_delivname',
    ]
    
    # Get numeric columns
    feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove excluded columns
    feature_cols = [col for col in feature_cols if col not in exclude_columns]
    
    return feature_cols


def create_classification_pipeline():
    """Create sklearn pipeline for classification"""
    
    pipeline = Pipeline([
        ('select', ColumnSelector()),
        ('imputer', SelectiveImputer(strategy='median')),
        ('feature_eng', FeatureEngineer()),
        ('scaler', StandardScaler()),
    ])
    
    return pipeline


def create_regression_pipeline():
    """Create sklearn pipeline for regression"""
    
    pipeline = Pipeline([
        ('select', ColumnSelector()),
        ('imputer', SelectiveImputer(strategy='median')),
        ('feature_eng', FeatureEngineer()),
        ('scaler', StandardScaler()),
    ])
    
    return pipeline


def save_pipeline(pipeline, filepath):
    """Save pipeline to file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(pipeline, filepath)
    print(f"Pipeline saved to {filepath}")


def load_pipeline(filepath):
    """Load pipeline from file"""
    return joblib.load(filepath)


if __name__ == '__main__':
    # Test the preprocessing
    from download_data import download_koi_dataset
    
    filepath = download_koi_dataset()
    df, df_class = load_and_preprocess_data(filepath)
    
    print(f"Total samples: {len(df)}")
    print(f"Classification samples: {len(df_class)}")
    print(f"Number of features: {len(get_feature_columns(df))}")
