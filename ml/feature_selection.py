"""
Feature selection module for Exoplanet Intelligence System
"""
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif, f_regression, mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')


def select_features_classification(X, y, n_features=20):
    """
    Select best features for classification task using multiple methods
    
    Args:
        X: Feature DataFrame
        y: Target variable
        n_features: Number of features to select
    
    Returns:
        List of selected feature names
    """
    # Method 1: F-test (ANOVA)
    selector_f = SelectKBest(score_func=f_classif, k=min(n_features, X.shape[1]))
    selector_f.fit(X, y)
    f_scores = pd.Series(selector_f.scores_, index=X.columns).sort_values(ascending=False)
    
    # Method 2: Mutual Information
    selector_mi = SelectKBest(score_func=mutual_info_classif, k=min(n_features, X.shape[1]))
    selector_mi.fit(X, y)
    mi_scores = pd.Series(selector_mi.scores_, index=X.columns).sort_values(ascending=False)
    
    # Method 3: Random Forest importance
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    rf_importance = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    
    # Combine rankings
    rankings = pd.DataFrame({
        'f_score': f_scores.rank(ascending=False),
        'mi_score': mi_scores.rank(ascending=False),
        'rf_importance': rf_importance.rank(ascending=False)
    })
    
    # Average rank
    rankings['avg_rank'] = rankings.mean(axis=1)
    rankings = rankings.sort_values('avg_rank')
    
    selected_features = rankings.head(n_features).index.tolist()
    
    return selected_features, rankings


def select_features_regression(X, y, n_features=20):
    """
    Select best features for regression task using multiple methods
    
    Args:
        X: Feature DataFrame
        y: Target variable
        n_features: Number of features to select
    
    Returns:
        List of selected feature names
    """
    # Method 1: F-test (correlation)
    selector_f = SelectKBest(score_func=f_regression, k=min(n_features, X.shape[1]))
    selector_f.fit(X, y)
    f_scores = pd.Series(selector_f.scores_, index=X.columns).sort_values(ascending=False)
    
    # Method 2: Random Forest importance for regression
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    rf_importance = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    
    # Combine rankings
    rankings = pd.DataFrame({
        'f_score': f_scores.rank(ascending=False),
        'rf_importance': rf_importance.rank(ascending=False)
    })
    
    # Average rank
    rankings['avg_rank'] = rankings.mean(axis=1)
    rankings = rankings.sort_values('avg_rank')
    
    selected_features = rankings.head(n_features).index.tolist()
    
    return selected_features, rankings


def get_top_features_for_api():
    """
    Get the most important features for the API input form
    These are hand-picked based on domain knowledge and typical importance
    """
    
    # Key features for exoplanet classification and radius prediction
    important_features = [
        # Planetary properties
        {
            'name': 'koi_prad',
            'description': 'Planetary radius (Earth radii)',
            'unit': 'Earth radii',
            'min': 0.1,
            'max': 30,
            'typical': 2.0
        },
        {
            'name': 'koi_depth',
            'description': 'Transit depth (parts per million)',
            'unit': 'ppm',
            'min': 0,
            'max': 10000,
            'typical': 100
        },
        {
            'name': 'koi_period',
            'description': 'Orbital period (days)',
            'unit': 'days',
            'min': 0.1,
            'max': 1000,
            'typical': 50
        },
        
        # Stellar properties
        {
            'name': 'koi_srad',
            'description': 'Stellar radius (solar radii)',
            'unit': 'Solar radii',
            'min': 0.1,
            'max': 10,
            'typical': 1.0
        },
        {
            'name': 'koi_steff',
            'description': 'Stellar effective temperature (K)',
            'unit': 'Kelvin',
            'min': 2500,
            'max': 10000,
            'typical': 5778
        },
        {
            'name': 'koi_smass',
            'description': 'Stellar mass (solar masses)',
            'unit': 'Solar masses',
            'min': 0.1,
            'max': 5,
            'typical': 1.0
        },
        {
            'name': 'koi_slogg',
            'description': 'Stellar surface gravity (log g)',
            'unit': 'log(g)',
            'min': 1,
            'max': 5,
            'typical': 4.5
        },
        {
            'name': 'koi_lum',
            'description': 'Stellar luminosity (log solar)',
            'unit': 'log(L☉)',
            'min': -3,
            'max': 5,
            'typical': 0
        },
        
        # Planet-star geometry
        {
            'name': 'koi_impact',
            'description': 'Impact parameter (b)',
            'unit': '',
            'min': 0,
            'max': 2,
            'typical': 0.5
        },
        {
            'name': 'koi_duration',
            'description': 'Transit duration (hours)',
            'unit': 'hours',
            'min': 0.1,
            'max': 50,
            'typical': 3
        },
        {
            'name': 'koi_dor',
            'description': 'Planet-star distance ratio (a/R*)',
            'unit': '',
            'min': 1,
            'max': 200,
            'typical': 20
        },
        
        # Signal properties
        {
            'name': 'koi_model_snr',
            'description': 'Model signal-to-noise ratio',
            'unit': '',
            'min': 0,
            'max': 500,
            'typical': 20
        },
        {
            'name': 'koi_max_mult_ev',
            'description': 'Maximum multiple event statistic',
            'unit': '',
            'min': 0,
            'max': 500,
            'typical': 50
        },
        {
            'name': 'koi_tce_plnt_num',
            'description': 'TCE planet number',
            'unit': '',
            'min': 1,
            'max': 7,
            'typical': 1
        },
        
        # Other important features
        {
            'name': 'koi_kepmag',
            'description': 'Kepler magnitude',
            'unit': 'mag',
            'min': 5,
            'max': 20,
            'typical': 14
        },
        {
            'name': 'koi_score',
            'description': 'Disposition score',
            'unit': '',
            'min': 0,
            'max': 1,
            'typical': 0.5
        },
        {
            'name': 'koi_qof',
            'description': 'Quality flag',
            'unit': '',
            'min': 0,
            'max': 1,
            'typical': 0.9
        },
    ]
    
    return important_features


if __name__ == '__main__':
    # Test feature selection
    from download_data import download_koi_dataset
    from preprocessing import load_and_preprocess_data, get_feature_columns
    import warnings
    warnings.filterwarnings('ignore')
    
    filepath = download_koi_dataset()
    df, df_class = load_and_preprocess_data(filepath)
    
    feature_cols = get_feature_columns(df_class)
    X = df_class[feature_cols]
    y = (df_class['koi_disposition'] == 'CONFIRMED').astype(int)
    
    selected_features, rankings = select_features_classification(X, y, n_features=15)
    print("Top 15 features for classification:")
    print(selected_features)
    
    # Regression
    y_reg = df['koi_prad']
    X_reg = df[feature_cols]
    selected_features_reg, rankings_reg = select_features_regression(X_reg, y_reg, n_features=15)
    print("\nTop 15 features for regression:")
    print(selected_features_reg)
