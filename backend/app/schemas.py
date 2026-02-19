"""
Pydantic Schemas for Exoplanet Intelligence System
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class TaskType(str, Enum):
    """Task type enumeration"""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"


class ClassificationRequest(BaseModel):
    """Request schema for classification prediction"""
    features: Dict[str, float] = Field(
        ...,
        description="Dictionary of input features for the exoplanet",
        example={
            "koi_prad": 2.5,
            "koi_depth": 150.0,
            "koi_period": 45.2,
            "koi_srad": 1.2,
            "koi_steff": 5800,
            "koi_smass": 1.1,
            "koi_slogg": 4.3,
            "koi_lum": 0.15,
            "koi_impact": 0.3,
            "koi_duration": 3.5,
            "koi_dor": 25.0,
            "koi_model_snr": 25.0,
            "koi_max_mult_ev": 50.0,
            "koi_tce_plnt_num": 1,
            "koi_kepmag": 14.0,
            "koi_score": 0.8,
            "koi_qof": 0.95
        }
    )
    
    @validator('features')
    def validate_features(cls, v):
        if not v:
            raise ValueError("Features cannot be empty")
        return v


class ClassificationResponse(BaseModel):
    """Response schema for classification prediction"""
    prediction: str = Field(..., description="Predicted class (CONFIRMED or FALSE POSITIVE)")
    probabilities: Dict[str, float] = Field(..., description="Probability scores for each class")
    confidence: float = Field(..., description="Confidence score (0-1)")
    model_version: str = Field(default="1.0.0", description="Model version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Prediction timestamp")


class RegressionRequest(BaseModel):
    """Request schema for regression prediction"""
    features: Dict[str, float] = Field(
        ...,
        description="Dictionary of input features for the exoplanet",
        example={
            "koi_prad": 2.5,
            "koi_depth": 150.0,
            "koi_period": 45.2,
            "koi_srad": 1.2,
            "koi_steff": 5800,
            "koi_smass": 1.1,
            "koi_slogg": 4.3,
            "koi_lum": 0.15,
            "koi_impact": 0.3,
            "koi_duration": 3.5,
            "koi_dor": 25.0,
            "koi_model_snr": 25.0,
            "koi_max_mult_ev": 50.0,
            "koi_tce_plnt_num": 1,
            "koi_kepmag": 14.0,
            "koi_score": 0.8,
            "koi_qof": 0.95
        }
    )
    
    @validator('features')
    def validate_features(cls, v):
        if not v:
            raise ValueError("Features cannot be empty")
        return v


class RegressionResponse(BaseModel):
    """Response schema for regression prediction"""
    prediction: float = Field(..., description="Predicted planetary radius (Earth radii)")
    confidence_interval: Dict[str, float] = Field(..., description="95% confidence interval")
    unit: str = Field(default="Earth radii", description="Unit of prediction")
    model_version: str = Field(default="1.0.0", description="Model version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Prediction timestamp")


class PredictionHistory(BaseModel):
    """Schema for prediction history"""
    id: int = Field(..., description="Prediction ID")
    task_type: str = Field(..., description="Task type (classification/regression)")
    input_features: Dict[str, Any] = Field(..., description="Input features")
    output_result: Dict[str, Any] = Field(..., description="Prediction output")
    model_name: str = Field(..., description="Model used")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type classification")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class HealthCheck(BaseModel):
    """Schema for health check response"""
    status: str = Field(..., description="Service status")
    database: Optional[str] = Field(None, description="Database status")
    models_loaded: Optional[bool] = Field(None, description="Models loaded status")


class ModelInfo(BaseModel):
    """Schema for model information"""
    classification_model: str = Field(..., description="Classification model name")
    regression_model: str = Field(..., description="Regression model name")
    classification_metrics: Optional[Dict[str, float]] = Field(None, description="Classification metrics")
    regression_metrics: Optional[Dict[str, float]] = Field(None, description="Regression metrics")
    features: Optional[List[str]] = Field(None, description="Feature names")
