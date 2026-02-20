"""
API Routes for Exoplanet Intelligence System
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import asyncio

from schemas import (
    ClassificationRequest,
    ClassificationResponse,
    RegressionRequest,
    RegressionResponse,
    PredictionHistory,
    ErrorResponse
)
from model_loader import predict_classification, predict_regression, get_model_info
from crud import save_prediction, get_prediction_history
from utils import validate_features, format_prediction_response

# Create router
router = APIRouter()


@router.post(
    "/predict/classification",
    response_model=ClassificationResponse,
    summary="Predict exoplanet classification",
    description="Predict whether an exoplanet candidate is CONFIRMED or FALSE POSITIVE"
)
async def classification_predict(request: ClassificationRequest):
    """
    Predict exoplanet classification
    
    - **features**: Dictionary of input features for the exoplanet
    
    Returns predicted class and probability scores
    """
    try:
        # Validate input features
        validated_features = validate_features(request.features)
        
        # Convert to DataFrame
        df = pd.DataFrame([validated_features])
        
        # Make prediction
        result = predict_classification(df)
        
        # Save to database
        await save_prediction(
            task_type="classification",
            input_features=validated_features,
            output_result=result,
            model_name="classification_pipeline"
        )
        
        # Format response
        response = format_prediction_response(result, "classification")
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post(
    "/predict/regression",
    response_model=RegressionResponse,
    summary="Predict planetary radius",
    description="Predict planetary radius in Earth radii"
)
async def regression_predict(request: RegressionRequest):
    """
    Predict planetary radius
    
    - **features**: Dictionary of input features for the exoplanet
    
    Returns predicted radius with confidence interval
    """
    try:
        # Validate input features
        validated_features = validate_features(request.features)
        
        # Convert to DataFrame
        df = pd.DataFrame([validated_features])
        
        # Make prediction
        result = predict_regression(df)
        
        # Save to database
        await save_prediction(
            task_type="regression",
            input_features=validated_features,
            output_result=result,
            model_name="regression_pipeline"
        )
        
        # Format response
        response = format_prediction_response(result, "regression")
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get(
    "/predictions/history",
    response_model=List[PredictionHistory],
    summary="Get prediction history",
    description="Retrieve history of all predictions"
)
async def get_history(limit: int = 50, offset: int = 0):
    """
    Get prediction history
    
    - **limit**: Maximum number of records to return
    - **offset**: Number of records to skip
    
    Returns list of past predictions
    """
    try:
        history = await get_prediction_history(limit=limit, offset=offset)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")


@router.get(
    "/models/info",
    summary="Get model information",
    description="Get information about loaded ML models"
)
async def model_info():
    """Get information about the loaded models"""
    try:
        info = get_model_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")


# Error response models
@router.get("/error/example")
async def error_example():
    """Example error response"""
    return ErrorResponse(
        error="Example Error",
        message="This is an example error response",
        type="ValidationError"
    )
