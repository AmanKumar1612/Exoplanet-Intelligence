"""
Train Classification Model for Exoplanet Intelligence System
Predicts whether an exoplanet candidate is CONFIRMED or FALSE POSITIVE
Target: koi_disposition
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    f1_score, accuracy_score, precision_score, recall_score
)
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from download_data import download_koi_dataset
from preprocessing import (
    load_and_preprocess_data, get_feature_columns, 
    create_classification_pipeline, SelectiveImputer, FeatureEngineer
)
from feature_selection import select_features_classification


def prepare_classification_data(df, feature_cols, selected_features=None):
    """Prepare data for classification"""
    
    # Filter to binary classification (CONFIRMED vs FALSE POSITIVE)
    df_binary = df[df['koi_disposition'].isin(['CONFIRMED', 'FALSE POSITIVE'])].copy()
    
    # Use selected features or all features
    if selected_features:
        use_features = [f for f in selected_features if f in feature_cols]
    else:
        use_features = feature_cols
    
    X = df_binary[use_features].copy()
    
    # Create binary target (1 = CONFIRMED, 0 = FALSE POSITIVE)
    y = (df_binary['koi_disposition'] == 'CONFIRMED').astype(int)
    
    return X, y, use_features


def train_classification_model(X, y):
    """Train and evaluate classification model"""
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("=" * 60)
    print("CLASSIFICATION MODEL TRAINING")
    print("=" * 60)
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Features: {X.shape[1]}")
    print(f"Class distribution (train): {dict(y_train.value_counts())}")
    
    # Create preprocessing pipeline
    preprocessing_pipeline = create_classification_pipeline()
    
    # Apply preprocessing
    X_train_processed = preprocessing_pipeline.fit_transform(X_train)
    X_test_processed = preprocessing_pipeline.transform(X_test)
    
    # Handle any remaining NaN values
    imputer = SelectiveImputer(strategy='median')
    X_train_processed = imputer.fit_transform(X_train_processed)
    X_test_processed = imputer.transform(X_test_processed)
    
    # Try multiple models
    models = {
        'RandomForest': RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        ),
        'XGBoost': XGBClassifier(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=1,
            random_state=42,
            n_jobs=-1,
            use_label_encoder=False,
            eval_metric='logloss'
        ),
        'GradientBoosting': GradientBoostingClassifier(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42
        )
    }
    
    best_model = None
    best_f1 = 0
    best_model_name = ""
    results = {}
    
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        
        # Cross-validation
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(model, X_train_processed, y_train, cv=cv, scoring='f1')
        
        # Train model
        model.fit(X_train_processed, y_train)
        
        # Predict
        y_pred = model.predict(X_test_processed)
        y_pred_proba = model.predict_proba(X_test_processed)[:, 1]
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        try:
            roc_auc = roc_auc_score(y_test, y_pred_proba)
        except:
            roc_auc = 0
        
        results[name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'cv_f1_mean': cv_scores.mean(),
            'cv_f1_std': cv_scores.std()
        }
        
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        print(f"  ROC-AUC: {roc_auc:.4f}")
        print(f"  CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_model_name = name
    
    print(f"\n*** Best Model: {best_model_name} (F1: {best_f1:.4f}) ***")
    
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
        best_model, param_grid, cv=3, scoring='f1', n_jobs=-1
    )
    grid_search.fit(X_train_processed, y_train)
    
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best CV F1: {grid_search.best_score_:.4f}")
    
    # Final model
    final_model = grid_search.best_estimator_
    
    # Final evaluation
    y_pred_final = final_model.predict(X_test_processed)
    y_pred_proba_final = final_model.predict_proba(X_test_processed)[:, 1]
    
    print("\n" + "=" * 60)
    print("FINAL MODEL EVALUATION")
    print("=" * 60)
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred_final, target_names=['FALSE POSITIVE', 'CONFIRMED']))
    
    print(f"\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred_final)
    print(cm)
    
    final_f1 = f1_score(y_test, y_pred_final)
    final_roc_auc = roc_auc_score(y_test, y_pred_proba_final)
    
    print(f"\nFinal F1-Score: {final_f1:.4f}")
    print(f"Final ROC-AUC: {final_roc_auc:.4f}")
    
    # Create full pipeline
    from sklearn.pipeline import Pipeline
    
    full_pipeline = Pipeline([
        ('preprocessing', preprocessing_pipeline),
        ('imputer', imputer),
        ('classifier', final_model)
    ])
    
    return full_pipeline, results, {
        'f1': final_f1,
        'roc_auc': final_roc_auc,
        'feature_names': list(X.columns)
    }


def save_classification_model(pipeline, metrics, output_dir='../backend/models'):
    """Save the trained classification model"""
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, 'classification_pipeline.pkl')
    joblib.dump(pipeline, model_path)
    
    metrics_path = os.path.join(output_dir, 'classification_metrics.pkl')
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
    X_raw = df_class[feature_cols]
    y_raw = (df_class['koi_disposition'] == 'CONFIRMED').astype(int)
    
    selected_features, rankings = select_features_classification(X_raw, y_raw, n_features=20)
    print(f"Selected features: {selected_features}")
    
    # Prepare data
    X, y, used_features = prepare_classification_data(df_class, feature_cols, selected_features)
    
    # Train model
    pipeline, results, metrics = train_classification_model(X, y)
    
    # Save model
    save_classification_model(pipeline, metrics)
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    
    return pipeline, results, metrics


if __name__ == '__main__':
    main()
