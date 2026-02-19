-- Seed data for Exoplanet Intelligence System
-- This file contains sample predictions for testing

-- Insert sample classification prediction
INSERT INTO predictions (task_type, input_features, output_result, model_name, created_at)
VALUES (
    'classification',
    '{
        "koi_prad": 2.5,
        "koi_depth": 150,
        "koi_period": 45.3,
        "koi_srad": 1.2,
        "koi_steff": 5800,
        "koi_smass": 1.1,
        "koi_slogg": 4.3,
        "koi_lum": 0.1,
        "koi_impact": 0.6,
        "koi_duration": 3.5,
        "koi_dor": 22.5,
        "koi_model_snr": 25.0,
        "koi_kepmag": 14.2,
        "koi_score": 0.85
    }'::jsonb,
    '{
        "prediction": "CONFIRMED",
        "confidence": 0.92,
        "probabilities": {
            "CONFIRMED": 0.92,
            "FALSE POSITIVE": 0.08
        }
    }'::jsonb,
    'classification_pipeline_v1',
    CURRENT_TIMESTAMP - INTERVAL '1 day'
);

-- Insert sample regression prediction
INSERT INTO predictions (task_type, input_features, output_result, model_name, created_at)
VALUES (
    'regression',
    '{
        "koi_prad": 2.5,
        "koi_depth": 150,
        "koi_period": 45.3,
        "koi_srad": 1.2,
        "koi_steff": 5800,
        "koi_smass": 1.1,
        "koi_slogg": 4.3,
        "koi_lum": 0.1,
        "koi_impact": 0.6,
        "koi_duration": 3.5,
        "koi_dor": 22.5,
        "koi_model_snr": 25.0,
        "koi_kepmag": 14.2,
        "koi_score": 0.85
    }'::jsonb,
    '{
        "prediction": 2.47,
        "confidence_interval": {
            "lower": 2.15,
            "upper": 2.79
        },
        "unit": "Earth radii"
    }'::jsonb,
    'regression_pipeline_v1',
    CURRENT_TIMESTAMP - INTERVAL '2 days'
);

-- Insert another classification prediction
INSERT INTO predictions (task_type, input_features, output_result, model_name, created_at)
VALUES (
    'classification',
    '{
        "koi_prad": 1.2,
        "koi_depth": 50,
        "koi_period": 12.5,
        "koi_srad": 0.9,
        "koi_steff": 5500,
        "koi_smass": 0.95,
        "koi_slogg": 4.5,
        "koi_lum": -0.2,
        "koi_impact": 0.3,
        "koi_duration": 2.8,
        "koi_dor": 15.0,
        "koi_model_snr": 18.5,
        "koi_kepmag": 13.8,
        "koi_score": 0.65
    }'::jsonb,
    '{
        "prediction": "FALSE POSITIVE",
        "confidence": 0.78,
        "probabilities": {
            "CONFIRMED": 0.22,
            "FALSE POSITIVE": 0.78
        }
    }'::jsonb,
    'classification_pipeline_v1',
    CURRENT_TIMESTAMP - INTERVAL '3 days'
);
