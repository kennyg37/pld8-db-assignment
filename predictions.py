import requests
import pickle
import numpy as np
import pandas as pd
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Load the trained model and normalization parameters
try:
    with open("model/model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
except Exception as e:
    logger.error(f"Failed to load model: {e}")

try:
    with open("model/normalization_params.pkl", "rb") as norm_file:
        normalization_params = pickle.load(norm_file)
except Exception as e:
    logger.error(f"Failed to load normalization parameters: {e}")

# Load location_freq from JSON file
with open('location_freq.json', 'r') as f:
    location_freq = json.load(f)

# Define mapping from dataset columns to JSON keys
KEY_MAPPING = {
    "name": "customer name",
    "email": "customer e-mail",
    "country_id": "country",
    "gender": "gender",
    "age": "age",
    "annual_salary": "annual Salary",
    "credit_card": "credit card debt",
    "net_worth": "net worth"
}

def normalize_data(data, normalization_params):
    """Normalize input data using min-max scaling based on normalization parameters."""
    try:
        for param_key, data_key in KEY_MAPPING.items():
            if param_key in normalization_params:
                min_val = float(normalization_params[param_key]["min"])
                max_val = float(normalization_params[param_key]["max"])
                data[data_key] = (data[data_key] - min_val) / (max_val - min_val)
        return data
    except Exception as e:
        logger.error(f"Unexpected error in normalize_data: {e}")
        return None

# Endpoint to fetch the latest user data
ENDPOINT_URL = 'https://car-sales-0zvx.onrender.com/users'

def fetch_latest_user_data():
    """Fetch the latest user data from the endpoint."""
    try:
        response = requests.get(ENDPOINT_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch latest user data: {e}")
        return None

def prepare_data_for_prediction(data):
    try:
        # Define expected columns based on normalization_params and additional fields
        expected_columns = list(normalization_params.keys()) + ["gender", "country"]

        # Convert JSON data to DataFrame, filling missing keys with 0
        df = pd.DataFrame([{json_key: data.get(json_key, 0) for json_key in KEY_MAPPING.keys()}])

        # Rename columns and apply mappings
        df.rename(columns=KEY_MAPPING, inplace=True)
        if "gender" in df.columns:
            df["gender"] = df["gender"].map({"Male": 1, "Female": 0}).fillna(0)
        if "country" in df.columns:
            df["country"] = df["country"].map(location_freq).fillna(0)

        # Ensure DataFrame includes all expected columns, filling missing ones with 0
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_columns].astype(float)

        # Normalize data
        normalized_data = normalize_data(df.to_dict(orient='records')[0], normalization_params)
        if normalized_data is not None:
            return np.array([list(normalized_data.values())])
    except Exception as e:
        logger.error(f"Error preparing data for prediction: {e}")
        return None

def predict_car_purchase():
    data = fetch_latest_user_data()
    if data:
        input_data = prepare_data_for_prediction(data)
        if input_data is not None:
            try:
                prediction = model.predict(input_data)
                print(f"Predicted car purchase amount for latest user: ${prediction[0]:.2f}")
            except Exception as e:
                logger.error(f"Prediction failed: {e}")
        else:
            logger.warning("Prediction could not be made due to missing or invalid input data.")
    else:
        logger.warning("Prediction could not be made due to missing data.")

# Run prediction for the latest user
predict_car_purchase()
