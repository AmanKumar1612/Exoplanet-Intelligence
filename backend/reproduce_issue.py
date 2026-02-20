import requests
import json

url = "http://127.0.0.1:8000/api/predict/classification"

# Payload from frontend (MISSING koi_qof)
payload_missing_feature = {
    "features": {
        "koi_prad": 2.5,
        "koi_depth": 100.0,
        "koi_period": 50.0,
        "koi_srad": 1.0,
        "koi_steff": 5778,
        "koi_smass": 1.0,
        "koi_slogg": 4.5,
        "koi_lum": 0.0,
        "koi_impact": 0.5,
        "koi_duration": 3.0,
        "koi_dor": 20.0,
        "koi_model_snr": 20.0,
        "koi_kepmag": 14.0,
        "koi_score": 0.5
        # koi_qof is missing
    }
}

# Payload with all features
payload_correct = {
    "features": {
        "koi_prad": 2.5,
        "koi_depth": 100.0,
        "koi_period": 50.0,
        "koi_srad": 1.0,
        "koi_steff": 5778,
        "koi_smass": 1.0,
        "koi_slogg": 4.5,
        "koi_lum": 0.0,
        "koi_impact": 0.5,
        "koi_duration": 3.0,
        "koi_dor": 20.0,
        "koi_model_snr": 20.0,
        "koi_kepmag": 14.0,
        "koi_score": 0.5,
        "koi_qof": 0.9
    }
}

print("Testing with missing feature...")
try:
    response = requests.post(url, json=payload_missing_feature)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\nTesting with correct features...")
try:
    response = requests.post(url, json=payload_correct)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
