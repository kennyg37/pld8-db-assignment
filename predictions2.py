import requests
import pickle
import numpy as np
import pandas as pd

# Load the trained model and normalization parameters
with open("model/model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("model/normalization_params.pkl", "rb") as norm_file:
    normalization_params = pickle.load(norm_file)

# Expected columns for model input
FEATURE_COLUMNS = ["age", "annual_salary", "credit_card", "net_worth"]

def normalize_data(data, normalization_params):
    """Normalize input data using saved normalization parameters."""
    for key in normalization_params:
        if key in data:
            mean, std = normalization_params[key]
            data[key] = (data[key] - mean) / std
    return data

def prepare_data_for_prediction(data):
    # Extract relevant features in the correct order and normalize
    input_data = {col: data[col] for col in FEATURE_COLUMNS}
    input_data = normalize_data(input_data, normalization_params)
    return np.array([list(input_data.values())])


ENDPOINT_URL = 'https://car-sales-0zvx.onrender.com/'


# Script 2 - fetch latest entry data automatically
def fetch_latest_entry():
    response = requests.get(f"{ENDPOINT_URL}/latest")
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch the latest entry data.")
        return None

def predict_latest_car_purchase():
    data = fetch_latest_entry()
    if data:
        input_data = prepare_data_for_prediction(data)
        prediction = model.predict(input_data)
        print(f"Predicted car purchase amount for the latest entry: ${prediction[0]:.2f}")
    else:
        print("Prediction could not be made due to missing data.")

# Example usage
predict_latest_car_purchase()
