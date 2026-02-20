import requests
import json

url = "http://127.0.0.1:8000/api/predict/classification"

def test_payload(name, payload):
    print(f"\n--- Testing {name} ---")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error Response: {response.text}")
        else:
            print("Success")
    except Exception as e:
        print(f"Request failed: {e}")

# 1. Fixed Payload (With koi_qof)
payload_fixed = {
    "features": {
        "koi_prad": 2.5,
        "koi_depth": 100.0,
        "koi_period": 50.0,
        "koi_srad": 1.0,
        "koi_steff": 5778.0,
        "koi_smass": 1.0,
        "koi_slogg": 4.5,
        "koi_lum": 0.0,
        "koi_impact": 0.5,
        "koi_duration": 3.0,
        "koi_dor": 20.0,
        "koi_model_snr": 20.0,
        "koi_kepmag": 14.0,
        "koi_score": 0.5,
        "koi_qof": 0.9  # Added
    }
}

test_payload("Fixed Payload (With koi_qof)", payload_fixed)
