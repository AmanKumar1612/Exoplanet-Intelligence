"""
Create dummy model files for testing the backend.
These are placeholder models that return random predictions.
In production, you would train real models using the training scripts.
"""
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Create dummy classification model
print("Creating dummy classification model...")
X_class = np.random.rand(100, 14)
y_class = np.random.choice(['CONFIRMED', 'FALSE POSITIVE'], 100)

# Create a simple pipeline with scaler and classifier
scaler = StandardScaler()
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(scaler.fit_transform(X_class), y_class)

classification_pipeline = Pipeline([
    ('scaler', scaler),
    ('classifier', clf)
])

joblib.dump(classification_pipeline, 'backend/models/classification_pipeline.pkl')
print("Created classification_pipeline.pkl")

# Create dummy regression model
print("Creating dummy regression model...")
X_reg = np.random.rand(100, 14)
y_reg = np.random.rand(100) * 5  # Random radius between 0 and 5

scaler_reg = StandardScaler()
reg = RandomForestRegressor(n_estimators=10, random_state=42)
reg.fit(scaler_reg.fit_transform(X_reg), y_reg)

regression_pipeline = Pipeline([
    ('scaler', scaler_reg),
    ('regressor', reg)
])

joblib.dump(regression_pipeline, 'backend/models/regression_pipeline.pkl')
print("Created regression_pipeline.pkl")

print("Done! Model files created successfully.")
