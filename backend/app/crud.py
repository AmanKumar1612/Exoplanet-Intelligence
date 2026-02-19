"""
CRUD Operations for Exoplanet Intelligence System
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from database import save_prediction_db, get_predictions_db, get_prediction_by_id_db


async def save_prediction(
    task_type: str,
    input_features: Dict[str, Any],
    output_result: Dict[str, Any],
    model_name: str
) -> int:
    """
    Save a prediction to the database
    
    Args:
        task_type: Type of prediction (classification/regression)
        input_features: Input features used for prediction
        output_result: Prediction output
        model_name: Name of the model used
    
    Returns:
        ID of the saved prediction
    """
    return await save_prediction_db(task_type, input_features, output_result, model_name)


async def get_prediction_history(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Get prediction history
    
    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
    
    Returns:
        List of prediction records
    """
    predictions = await get_predictions_db(limit=limit, offset=offset)
    
    # Format response
    formatted_predictions = []
    for pred in predictions:
        formatted_predictions.append({
            "id": pred.get("id"),
            "task_type": pred.get("task_type"),
            "input_features": pred.get("input_features"),
            "output_result": pred.get("output_result"),
            "model_name": pred.get("model_name"),
            "created_at": pred.get("created_at") if isinstance(pred.get("created_at"), datetime) else datetime.fromisoformat(pred.get("created_at", datetime.utcnow().isoformat()))
        })
    
    return formatted_predictions


async def get_prediction(prediction_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a specific prediction by ID
    
    Args:
        prediction_id: ID of the prediction
    
    Returns:
        Prediction record or None if not found
    """
    pred = await get_prediction_by_id_db(prediction_id)
    
    if pred:
        return {
            "id": pred.get("id"),
            "task_type": pred.get("task_type"),
            "input_features": pred.get("input_features"),
            "output_result": pred.get("output_result"),
            "model_name": pred.get("model_name"),
            "created_at": pred.get("created_at") if isinstance(pred.get("created_at"), datetime) else datetime.fromisoformat(pred.get("created_at", datetime.utcnow().isoformat()))
        }
    
    return None


async def get_predictions_by_task(task_type: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get predictions filtered by task type
    
    Args:
        task_type: Type of prediction (classification/regression)
        limit: Maximum number of records
    
    Returns:
        List of predictions for the specified task type
    """
    all_predictions = await get_predictions_db(limit=1000)
    return [p for p in all_predictions if p.get("task_type") == task_type][:limit]


async def delete_prediction(prediction_id: int) -> bool:
    """
    Delete a prediction by ID
    
    Args:
        prediction_id: ID of the prediction to delete
    
    Returns:
        True if deleted, False otherwise
    """
    # Note: Implement delete logic if needed
    # For now, this is a placeholder
    return False
