# Exoplanet Intelligence System - API Documentation

## Base URL

```
Production: https://your-backend-url.onrender.com
Development: http://localhost:8000
```

## Endpoints

### Health Check

Check if the API is running.

**GET** `/api/health`

**Response:**
```
json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### Classification Prediction

Predict whether an exoplanet candidate is CONFIRMED or FALSE POSITIVE.

**POST** `/api/predict/classification`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```
json
{
  "features": {
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
  }
}
```

**Response:**
```
json
{
  "prediction": "CONFIRMED",
  "confidence": 0.92,
  "probabilities": {
    "CONFIRMED": 0.92,
    "FALSE POSITIVE": 0.08
  },
  "model_name": "classification_pipeline_v1",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Error Response:**
```
json
{
  "detail": "Error message describing what went wrong"
}
```

---

### Regression Prediction

Predict planetary radius in Earth radii.

**POST** `/api/predict/regression`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```
json
{
  "features": {
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
  }
}
```

**Response:**
```
json
{
  "prediction": 2.47,
  "confidence_interval": {
    "lower": 2.15,
    "upper": 2.79
  },
  "unit": "Earth radii",
  "model_name": "regression_pipeline_v1",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Error Response:**
```
json
{
  "detail": "Error message describing what went wrong"
}
```

---

### Prediction History

Get prediction history from the database.

**GET** `/api/predictions/history`

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | int | 50 | Maximum number of records |
| offset | int | 0 | Number of records to skip |

**Response:**
```
json
[
  {
    "id": 1,
    "task_type": "classification",
    "input_features": {...},
    "output_result": {
      "prediction": "CONFIRMED",
      "confidence": 0.92
    },
    "model_name": "classification_pipeline_v1",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### Model Information

Get information about the deployed models.

**GET** `/api/models/info`

**Response:**
```
json
{
  "classification": {
    "model_name": "classification_pipeline_v1",
    "model_type": "RandomForestClassifier",
    "features": ["koi_prad", "koi_depth", ...],
    "f1_score": 0.95,
    "roc_auc": 0.98
  },
  "regression": {
    "model_name": "regression_pipeline_v1",
    "model_type": "XGBRegressor",
    "features": ["koi_prad", "koi_depth", ...],
    "rmse": 0.35,
    "mae": 0.28
  }
}
```

---

## Feature Descriptions

| Feature | Unit | Range | Description |
|---------|------|-------|-------------|
| koi_prad | Earth radii | 0.1 - 30 | Planetary radius |
| koi_depth | ppm | 0 - 10000 | Transit depth |
| koi_period | days | 0.1 - 1000 | Orbital period |
| koi_srad | Solar radii | 0.1 - 10 | Stellar radius |
| koi_steff | Kelvin | 2500 - 10000 | Stellar effective temperature |
| koi_smass | Solar masses | 0.1 - 5 | Stellar mass |
| koi_slogg | log(g) | 1 - 5 | Surface gravity |
| koi_lum | log(L☉) | -3 - 5 | Stellar luminosity |
| koi_impact | - | 0 - 2 | Impact parameter |
| koi_duration | hours | 0.1 - 50 | Transit duration |
| koi_dor | - | 1 - 200 | Planet-star distance ratio |
| koi_model_snr | - | 0 - 500 | Signal-to-noise ratio |
| koi_kepmag | mag | 5 - 20 | Kepler magnitude |
| koi_score | - | 0 - 1 | Disposition score |

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input |
| 422 | Validation Error |
| 500 | Internal Server Error |
| 503 | Service Unavailable |
| 504 | Gateway Timeout |

---

## Rate Limits

- **Development:** Unlimited
- **Production:** 100 requests/minute

---

## Support

For questions or issues, please contact the development team.
