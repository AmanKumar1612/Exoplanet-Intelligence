"""
Train Regression Model for Exoplanet Intelligence System
Predicts planetary radius (Earth radii)
Target: koi_prad
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from download_data import download_koi_dataset
from preprocessing import (
    load_and_preprocess_data, get_feature_columns, 
    create_regression_pipeline, SelectiveImputer, FeatureEngineer
)
from feature_selection import select_features_regression


def prepare_regression_data(df, feature_cols, selected_features=None):
    """Prepare data for regression"""
    
    # Use selected features or all features
    if selected_features:
        use_features = [f for f in selected_features if f in feature_cols]
    else:
        use_features = feature_cols
    
    # Filter out rows with missing target
    df_reg = df.dropna(subset=['koi_prad'])
    
    X = df_reg[use_features].copy()
    
    # Target variable
    y = df_reg['koi_prad']
    
    return X, y, use_features


def train_regression_model(X, y):
    """Train and evaluate regression model"""
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("=" * 60)
    print("REGRESSION MODEL TRAINING")
    print("=" * 60)
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Features: {X.shape[1]}")
    print(f"Target range: {y.min():.2f} - {y.max():.2f} Earth radii")
    print(f"Target mean: {y.mean():.2f} Earth radii")
    print(f"Target std: {y.std():.2f} Earth radii")
    
    # Create preprocessing pipeline
    preprocessing_pipeline = create_regression_pipeline()
    
    # Apply preprocessing
    X_train_processed = preprocessing_pipeline.fit_transform(X_train)
    X_test_processed = preprocessing_pipeline.transform(X_test)
    
    # Handle any remaining NaN values
    imputer = SelectiveImputer(strategy='median')
    X_train_processed = imputer.fit_transform(X_train_processed)
    X_test_processed = imputer.transform(X_test_processed)
    
    # Try multiple models
    models = {
        'RandomForest': RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ),
        'XGBoost': XGBRegressor(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        ),
        'GradientBoosting': GradientBoostingRegressor(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42
        )
    }
    
    best_model = None
    best_rmse = float('inf')
    best_model_name = ""
    results = {}
    
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train_processed, y_train, cv=5, scoring='neg_mean_squared_error')
        cv_rmse = np.sqrt(-cv_scores.mean())
        
        # Train model
        model.fit(X_train_processed, y_train)
        
        # Predict
        y_pred = model.predict(X_test_processed)
        
        # Metrics
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'cv_rmse': cv_rmse
        }
        
        print(f"  RMSE: {rmse:.4f}")
        print(f"  MAE: {mae:.4f}")
        print(f"  R2: {r2:.4f}")
        print(f"  CV RMSE: {cv_rmse:.4f}")
        
        if rmse < best_rmse:
            best_rmse = rmse
            best_model = model
            best_model_name = name
    
    print(f"\n*** Best Model: {best_model_name} (RMSE: {best_rmse:.4f}) ***")
    
    # Hyperparameter tuning for best model
    print("\n--- Hyperparameter Tuning ---")
    
    if best_model_name == 'RandomForest':
        param_grid = {
            'n_estimators': [150, 200, 250],
            'max_depth': [10, 15, 20],
            'min_samples_split': [3, 5, 7]
        }
    elif best_model_name == 'XGBoost':
        param_grid = {
            'n_estimators': [150, 200, 250],
            'max_depth': [6, 8, 10],
            'learning_rate': [0.05, 0.1, 0.15]
        }
    else:
        param_grid = {
            'n_estimators': [100, 150, 200],
            'max_depth': [4, 6, 8],
            'learning_rate': [0.05, 0.1, 0.15]
        }
    
    grid_search = GridSearchCV(
        best_model, param_grid, cv=3, scoring='neg_mean_squared_error', n_jobs=-1
    )
    grid_search.fit(X_train_processed, y_train)
    
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best CV RMSE: {np.sqrt(-grid_search.best_score_):.4f}")
    
    # Final model
    final_model = grid_search.best_estimator_
    
    # Final evaluation
    y_pred_final = final_model.predict(X_test_processed)
    
    final_rmse = np.sqrt(mean_squared_error(y_test, y_pred_final))
    final_mae = mean_absolute_error(y_test, y_pred_final)
    final_r2 = r2_score(y_test, y_pred_final)
    
    # Calculate confidence interval (prediction interval)
    residuals = y_test - y_pred_final
    std_error = np.std(residuals)
    
    print("\n" + "=" * 60)
    print("FINAL MODEL EVALUATION")
    print("=" * 60)
    print(f"\nRMSE: {final_rmse:.4f} Earth radii")
    print(f"MAE: {final_mae:.4f} Earth radii")
    print(f"R2: {final_r2:.4f}")
    print(f"Standard Error: {std_error:.4f} Earth radii")
    
    # Create full pipeline
    from sklearn.pipeline import Pipeline
    
    full_pipeline = Pipeline([
        ('preprocessing', preprocessing_pipeline),
        ('imputer', imputer),
        ('regressor', final_model)
    ])
    
    return full_pipeline, results, {
        'rmse': final_rmse,
        'mae': final_mae,
        'r2': final_r2,
        'std_error': std_error,
        'feature_names': list(X.columns)
    }


def save_regression_model(pipeline, metrics, output_dir='../backend/models'):
    """Save the trained regression model"""
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, 'regression_pipeline.pkl')
    joblib.dump(pipeline, model_path)
    
    metrics_path = os.path.join(output_dir, 'regression_metrics.pkl')
    joblib.dump(metrics, metrics_path)
    
    print(f"\nModel saved to: {model_path}")
    print(f"Metrics saved to: {metrics_path}")


def main():
    """Main training function"""
    print("Downloading dataset...")
    filepath = download_koi_dataset()
    
    print("\nLoading and preprocessing data...")
    df, df_class = load_and_preprocess_data(filepath)
    
    feature_cols = get_feature_columns(df_class)
    print(f"Available features: {len(feature_cols)}")
    
    # Feature selection
    print("\nPerforming feature selection...")
    X_raw = df[feature_cols]
    y_raw = df['koi_prad'].dropna()
    
    # Get common indices
    common_idx = X_raw.index.intersection(y_raw.index)
    X_raw = X_raw.loc[common_idx]
    y_raw = y_raw.loc[common_idx]
    
    selected_features, rankings = select_features_regression(X_raw, y_raw, n_features=20)
    print(f"Selected features: {selected_features}")
    
    # Prepare data
    X, y, used_features = prepare_regression_data(df, feature_cols, selected_features)
    
    # Train model
    pipeline, results, metrics = train_regression_model(X, y)
    
    # Save model
    save_regression_model(pipeline, metrics)
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    
    return pipeline, results, metrics


if __name__ == '__main__':
    main()
