"""
Mock Database Implementation for Exoplanet Intelligence System
Stores predictions in memory. Data will be lost on restart.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

# In-memory storage
PREDICTIONS_DB = []
ID_COUNTER = 1

async def save_prediction_db(
    task_type: str,
    input_features: Dict[str, Any],
    output_result: Dict[str, Any],
    model_name: str
) -> int:
    """
    Save a prediction to the in-memory database
    """
    global ID_COUNTER
    
    prediction_record = {
        "id": ID_COUNTER,
        "task_type": task_type,
        "input_features": input_features,
        "output_result": output_result,
        "model_name": model_name,
        "created_at": datetime.utcnow().isoformat()
    }
    
    PREDICTIONS_DB.append(prediction_record)
    new_id = ID_COUNTER
    ID_COUNTER += 1
    
    # Simulate DB latency
    await asyncio.sleep(0.01)
    
    return new_id

async def get_predictions_db(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Get predictions from in-memory database with pagination
    """
    # Simulate DB latency
    await asyncio.sleep(0.01)
    
    # Sort by created_at desc (newest first)
    sorted_predictions = sorted(
        PREDICTIONS_DB, 
        key=lambda x: x["created_at"], 
        reverse=True
    )
    
    return sorted_predictions[offset : offset + limit]

async def get_prediction_by_id_db(prediction_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a specific prediction by ID
    """
    # Simulate DB latency
    await asyncio.sleep(0.01)
    
    for pred in PREDICTIONS_DB:
        if pred["id"] == prediction_id:
            return pred
            
    return None


async def init_db():
    """
    Initialize the database connection
    """
    # Simulate DB initialization
    await asyncio.sleep(0.01)
    print("Database initialized (Mock)")


async def close_db():
    """
    Close the database connection
    """
    # Simulate DB closing
    await asyncio.sleep(0.01)
    print("Database connection closed (Mock)")
