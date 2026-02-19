
"""
Train reliable ML models using synthetic data for Exoplanet Intelligence System.
Features are generated with realistic physical correlations.
"""
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

# Define feature list (must match frontend config)
FEATURES = [
    'koi_prad', 'koi_depth', 'koi_period', 'koi_srad', 'koi_steff',
    'koi_smass', 'koi_slogg', 'koi_lum', 'koi_impact', 'koi_duration',
    'koi_dor', 'koi_model_snr', 'koi_kepmag', 'koi_score', 'koi_qof'
]

def generate_synthetic_data(n_samples=2000):
    """Generate synthetic exoplanet data with physical correlations"""
    np.random.seed(42)
    
    data = {}
    
    # 1. Independent Features (distributions based on Kepler data)
    data['koi_period'] = np.random.exponential(scale=50, size=n_samples) + 0.5
    data['koi_srad'] = np.random.lognormal(mean=0, sigma=0.5, size=n_samples)  # Solar radii
    data['koi_steff'] = np.random.normal(loc=5700, scale=1000, size=n_samples) # Kelvin
    data['koi_smass'] = data['koi_srad'] ** 0.8 * np.random.normal(1, 0.1, n_samples) # Mass scales with Radius
    data['koi_slogg'] = 4.44 - np.log10(data['koi_srad']) + np.random.normal(0, 0.1, n_samples)
    data['koi_kepmag'] = np.random.uniform(8, 16, n_samples)
    data['koi_impact'] = np.random.uniform(0, 1.2, n_samples)
    data['koi_score'] = np.random.beta(a=2, b=2, size=n_samples) # Disposition score
    data['koi_qof'] = np.random.beta(a=5, b=1, size=n_samples) # Quality flag (mostly high)
    
    # 2. Dependent Features (Physics-based)
    
    # Planet Radius (Earth radii) - Log-uniform distribution + correlation with period
    data['koi_prad'] = np.exp(np.random.uniform(np.log(0.5), np.log(20), n_samples))
    
    # Transit Depth (ppm) ~ (Rp/Rs)^2
    # Depth = (Planet Radius / Star Radius)^2 * 10^6
    # Adding some noise
    ratio_sq = (data['koi_prad'] * 0.009158 / data['koi_srad']) ** 2  # 0.009158 converts Earth radii to Solar radii
    data['koi_depth'] = ratio_sq * 1e6 * np.random.normal(1, 0.1, n_samples)
    
    # Transit Duration ~ Period^(1/3) * Star Radius
    data['koi_duration'] = (data['koi_period'] ** (1/3)) * data['koi_srad'] * np.random.normal(3, 0.5, n_samples)
    
    # Distance Ratio (a/R*) ~ Period^(2/3) / Star Radius
    data['koi_dor'] = (data['koi_period'] ** (2/3)) * 10 / data['koi_srad']
    
    # Luminosity ~ Star Radius^2 * (Temp/5778)^4
    data['koi_lum'] = (data['koi_srad']**2) * ((data['koi_steff']/5778)**4)
    
    # SNR ~ Depth * sqrt(Duration) * 10^(-0.4 * (Mag - 12))
    snr_proxy = data['koi_depth'] * np.sqrt(data['koi_duration']) * (10 ** (-0.4 * (data['koi_kepmag'] - 12)))
    data['koi_model_snr'] = snr_proxy * np.random.normal(1, 0.2, n_samples)
    
    # 3. Targets
    
    # Classification Target: CONFIRMED (1) or FALSE POSITIVE (0)
    # Higher Score, SNR, and logical bounds increase probability of being Confirmed
    prob_confirmed = data['koi_score'] * 0.8 # Base probability from score
    
    # Penalize physically unlikely combinations (e.g. huge radius but low depth)
    mask_unlikely = (data['koi_prad'] > 25) | (data['koi_model_snr'] < 5)
    prob_confirmed[mask_unlikely] *= 0.1
    
    # Bonus for Earth-like planets
    mask_earthlike = (data['koi_prad'] < 2.5) & (data['koi_steff'] > 5000) & (data['koi_steff'] < 6500)
    prob_confirmed[mask_earthlike] += 0.2
    
    labels = (np.random.random(n_samples) < prob_confirmed).astype(int)
    
    # Regression Target: koi_prad (already generated)
    # We will try to predict this using other features, mainly Depth and Star Radius
    
    df = pd.DataFrame(data)
    
    # Ensure all features exist
    for col in FEATURES:
        if col not in df.columns:
            df[col] = 0
            
    return df, labels

def train_and_save_models():
    """Train models and save to disk"""
    print("Generating synthetic dataset...")
    df, labels = generate_synthetic_data(n_samples=5000)
    
    # Prepare Data
    X = df[FEATURES]
    y_class = labels
    y_reg = df['koi_prad']
    
    # Split Data
    X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
        X, y_class, y_reg, test_size=0.2, random_state=42
    )
    
    print("Training Classification Model...")
    clf_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10))
    ])
    clf_pipeline.fit(X_train, y_class_train)
    
    # Evaluate
    class_acc = accuracy_score(y_class_test, clf_pipeline.predict(X_test))
    print(f"Classification Accuracy: {class_acc:.4f}")
    
    print("Training Regression Model...")
    # For regression, we must drop the target 'koi_prad' from inputs if it was in FEATURES list
    # But wait! 'koi_prad' IS in FEATURES list in InputForm.jsx but for Regression task, 
    # we are predicting it. So we shouldn't use it as input for regression.
    # We will zero it out or remove it for regression training
    
    X_reg_train = X_train.copy()
    X_reg_test = X_test.copy()
    X_reg_train['koi_prad'] = 0 # Mask target in input
    X_reg_test['koi_prad'] = 0
    
    print(f"Regression Training Features: {X_reg_train.columns.tolist()}")
    
    reg_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10))
    ])
    reg_pipeline.fit(X_reg_train, y_reg_train)
    
    # Evaluate
    reg_mse = mean_squared_error(y_reg_test, reg_pipeline.predict(X_reg_test))
    print(f"Regression RMSE: {np.sqrt(reg_mse):.4f}")
    
    # Save Models
    model_dir = "models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    print(f"Saving models to {model_dir}...")
    joblib.dump(clf_pipeline, os.path.join(model_dir, "classification_pipeline.pkl"))
    joblib.dump(reg_pipeline, os.path.join(model_dir, "regression_pipeline.pkl"))
    
    # Save Metrics
    joblib.dump({"accuracy": class_acc}, os.path.join(model_dir, "classification_metrics.pkl"))
    joblib.dump({"rmse": np.sqrt(reg_mse)}, os.path.join(model_dir, "regression_metrics.pkl"))
    
    print("Done!")

if __name__ == "__main__":
    train_and_save_models()
