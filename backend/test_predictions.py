
import requests
import json
import sys

url = "http://127.0.0.1:8000/api/predict/regression"
headers = {"Content-Type": "application/json"}

# Base feature set with VALID values (koi_prad must be >= 0.1)
base_features = {
    "koi_period": 10,
    "koi_srad": 1.0,
    "koi_steff": 5700,
    "koi_smass": 1.0,
    "koi_slogg": 4.5,
    "koi_lum": 1.0,
    "koi_impact": 0.5,
    "koi_duration": 3,
    "koi_dor": 20,
    "koi_model_snr": 20,
    "koi_kepmag": 14,
    "koi_score": 1,
    "koi_prad": 1.0,  # Valid dummy value (> 0.1)
    "koi_qof": 0
}

def make_request(features):
    try:
        response = requests.post(url, json={"features": features}, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e), "text": response.text if 'response' in locals() else ""}

with open("test_output.txt", "w") as f:
    f.write("Testing Regression Model Variance...\n")

    # Request 1: Small Depth (100 ppm)
    features_small = base_features.copy()
    features_small["koi_depth"] = 100
    res_small = make_request(features_small)

    # Request 2: Large Depth (9000 ppm)
    features_large = base_features.copy()
    features_large["koi_depth"] = 9000
    res_large = make_request(features_large)

    pred_small = res_small.get("prediction", "ERROR")
    pred_large = res_large.get("prediction", "ERROR")

    f.write(f"Prediction (Depth=100):  {pred_small}\n")
    f.write(f"Prediction (Depth=9000): {pred_large}\n")
    
    f.write(f"Small Response: {json.dumps(res_small, indent=2)}\n")
    f.write(f"Large Response: {json.dumps(res_large, indent=2)}\n")

    if isinstance(pred_small, (int, float)) and isinstance(pred_large, (int, float)):
        if pred_large > pred_small:
            f.write("\nSUCCESS: Model responds to input change (Larger Depth -> Larger Radius)\n")
        else:
            f.write("\nFAILURE: Model yielded constant or unexpected output\n")
    else:
        f.write("\nERROR: Could not compare predictions.\n")
