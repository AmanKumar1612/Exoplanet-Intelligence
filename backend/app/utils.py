"""
Utility Functions for Exoplanet Intelligence System
"""
from typing import Dict, Any, List
import numpy as np
from datetime import datetime


# Feature definitions with validation rules
FEATURE_DEFINITIONS = {
    'koi_prad': {
        'name': 'Planetary Radius',
        'description': 'Radius of the planet in Earth radii',
        'unit': 'Earth radii',
        'min': 0.1,
        'max': 30,
        'typical': 2.0,
        'required': True
    },
    'koi_depth': {
        'name': 'Transit Depth',
        'description': 'Depth of the transit in parts per million (ppm)',
        'unit': 'ppm',
        'min': 0,
        'max': 10000,
        'typical': 100,
        'required': False
    },
    'koi_period': {
        'name': 'Orbital Period',
        'description': 'Time between successive transits',
        'unit': 'days',
        'min': 0.1,
        'max': 1000,
        'typical': 50,
        'required': False
    },
    'koi_srad': {
        'name': 'Stellar Radius',
        'description': 'Radius of the host star in solar radii',
        'unit': 'Solar radii',
        'min': 0.1,
        'max': 10,
        'typical': 1.0,
        'required': False
    },
    'koi_steff': {
        'name': 'Stellar Effective Temperature',
        'description': 'Effective temperature of the host star',
        'unit': 'Kelvin',
        'min': 2500,
        'max': 10000,
        'typical': 5778,
        'required': False
    },
    'koi_smass': {
        'name': 'Stellar Mass',
        'description': 'Mass of the host star in solar masses',
        'unit': 'Solar masses',
        'min': 0.1,
        'max': 5,
        'typical': 1.0,
        'required': False
    },
    'koi_slogg': {
        'name': 'Stellar Surface Gravity',
        'description': 'Surface gravity of the host star (log g)',
        'unit': 'log(g)',
        'min': 1,
        'max': 5,
        'typical': 4.5,
        'required': False
    },
    'koi_lum': {
        'name': 'Stellar Luminosity',
        'description': 'Luminosity of the host star (log solar)',
        'unit': 'log(L☉)',
        'min': -3,
        'max': 5,
        'typical': 0,
        'required': False
    },
    'koi_impact': {
        'name': 'Impact Parameter',
        'description': 'Impact parameter of the transit (b)',
        'unit': '',
        'min': 0,
        'max': 2,
        'typical': 0.5,
        'required': False
    },
    'koi_duration': {
        'name': 'Transit Duration',
        'description': 'Duration of the transit',
        'unit': 'hours',
        'min': 0.1,
        'max': 50,
        'typical': 3,
        'required': False
    },
    'koi_dor': {
        'name': 'Planet-Star Distance Ratio',
        'description': 'Ratio of orbital semi-major axis to stellar radius (a/R*)',
        'unit': '',
        'min': 1,
        'max': 200,
        'typical': 20,
        'required': False
    },
    'koi_model_snr': {
        'name': 'Model Signal-to-Noise Ratio',
        'description': 'Signal-to-noise ratio of the transit model',
        'unit': '',
        'min': 0,
        'max': 500,
        'typical': 20,
        'required': False
    },
    'koi_kepmag': {
        'name': 'Kepler Magnitude',
        'description': 'Kepler magnitude of the target',
        'unit': 'mag',
        'min': 5,
        'max': 20,
        'typical': 14,
        'required': False
    },
    'koi_score': {
        'name': 'Disposition Score',
        'description': 'Score for the disposition (probability of being a planet)',
        'unit': '',
        'min': 0,
        'max': 1,
        'typical': 0.5,
        'required': False
    },
    'koi_qof': {
        'name': 'Quality Flag',
        'description': 'Quality flag for the KOI',
        'unit': '',
        'min': 0,
        'max': 1,
        'typical': 0.9,
        'required': False
    }
}


def validate_features(features: Dict[str, float]) -> Dict[str, float]:
    """
    Validate and sanitize input features
    
    Args:
        features: Dictionary of input features
    
    Returns:
        Validated features dictionary
    
    Raises:
        ValueError: If validation fails
    """
    if not features:
        raise ValueError("Features cannot be empty")
    
    validated = {}
    
    for feature_name, feature_value in features.items():
        # Check if feature is defined
        if feature_name not in FEATURE_DEFINITIONS:
            # Allow unknown features but warn
            validated[feature_name] = float(feature_value)
            continue
        
        feature_def = FEATURE_DEFINITIONS[feature_name]
        
        # Check if value is numeric
        try:
            value = float(feature_value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid value for {feature_name}: must be a number")
        
        # Check range
        if feature_def['min'] is not None and value < feature_def['min']:
            raise ValueError(
                f"Value for {feature_name} ({value}) is below minimum ({feature_def['min']})"
            )
        
        if feature_def['max'] is not None and value > feature_def['max']:
            raise ValueError(
                f"Value for {feature_name} ({value}) exceeds maximum ({feature_def['max']})"
            )
        
        validated[feature_name] = value
    
    # Fill in default values for missing features
    for feature_name, feature_def in FEATURE_DEFINITIONS.items():
        if feature_name not in validated:
            validated[feature_name] = feature_def['typical']
    
    return validated


def format_prediction_response(result: Dict[str, Any], task_type: str) -> Dict[str, Any]:
    """
    Format prediction response for API
    
    Args:
        result: Prediction result from model
        task_type: Type of task (classification/regression)
    
    Returns:
        Formatted response dictionary
    """
    from datetime import datetime
    
    response = {
        "model_version": "1.0.0",
        "timestamp": datetime.utcnow()
    }
    
    if task_type == "classification":
        response["prediction"] = result.get("prediction")
        response["probabilities"] = result.get("probabilities")
        response["confidence"] = result.get("confidence")
    
    elif task_type == "regression":
        response["prediction"] = result.get("prediction")
        response["confidence_interval"] = result.get("confidence_interval")
        response["unit"] = result.get("unit", "Earth radii")
    
    return response


def get_feature_info() -> List[Dict[str, Any]]:
    """Get information about all features"""
    return [
        {
            "name": key,
            **value
        }
        for key, value in FEATURE_DEFINITIONS.items()
    ]


def calculate_confidence_interval(prediction: float, std_error: float, confidence: float = 0.95) -> Dict[str, float]:
    """
    Calculate confidence interval for regression prediction
    
    Args:
        prediction: Predicted value
        std_error: Standard error of prediction
        confidence: Confidence level (default 0.95 for 95%)
    
    Returns:
        Dictionary with lower and upper bounds
    """
    # Z-score for 95% confidence
    z_score = 1.96
    
    lower = prediction - z_score * std_error
    upper = prediction + z_score * std_error
    
    # Ensure non-negative values for radius
    lower = max(0.1, lower)
    
    return {
        "lower": round(lower, 4),
        "upper": round(upper, 4),
        "confidence": confidence
    }
