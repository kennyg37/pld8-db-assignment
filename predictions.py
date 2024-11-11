import requests
import pickle
import numpy as np
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Load the trained model and normalization parameters
try:
    with open("model/model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")

try:
    with open("model/normalization_params.pkl", "rb") as norm_file:
        normalization_params = pickle.load(norm_file)
    logger.info("Normalization parameters loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load normalization parameters: {e}")

def normalize_data(data, normalization_params):
    """Normalize input data using saved normalization parameters."""
    for key in normalization_params:
        mean, std = normalization_params[key]
        data[key] = (data[key] - mean) / std
    return data

ENDPOINT_URL = 'https://car-sales-0zvx.onrender.com'

# Script 1 - fetch data by user_id
def fetch_data_by_user_id(user_id):
    try:
        response = requests.get(f"{ENDPOINT_URL}/{user_id}")
        response.raise_for_status()
        data = response.json()
        logger.info(f"Data fetched successfully for user_id: {user_id}")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data for user_id {user_id}: {e}")
        return None

def prepare_data_for_prediction(data):
    try:
        # Extract relevant features and normalize
        input_data = {
            "age": data["age"],
            "annual_salary": data["annual_salary"],
            "credit_card": data["credit_card"],
            "net_worth": data["net_worth"],
        }
        input_data = normalize_data(input_data, normalization_params)
        logger.info("Data prepared and normalized for prediction.")
        return np.array([list(input_data.values())])
    except KeyError as e:
        logger.error(f"KeyError: Missing data field - {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while preparing data for prediction: {e}")
        return None

def predict_car_purchase(user_id):
    data = fetch_data_by_user_id(user_id)
    if data:
        input_data = prepare_data_for_prediction(data)
        if input_data is not None:
            try:
                prediction = model.predict(input_data)
                logger.info(f"Predicted car purchase amount for user_id {user_id}: ${prediction[0]:.2f}")
                print(f"Predicted car purchase amount for user_id {user_id}: ${prediction[0]:.2f}")
            except Exception as e:
                logger.error(f"Prediction failed for user_id {user_id}: {e}")
        else:
            logger.warning("Prediction could not be made due to missing or invalid input data.")
    else:
        logger.warning("Prediction could not be made due to missing data.")

# Example usage
user_id = "a5037dbf-cbde-401e-8b35-1058d7cb4c04"  # Replace with actual user_id
predict_car_purchase(user_id)
