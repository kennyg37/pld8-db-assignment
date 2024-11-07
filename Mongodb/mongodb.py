import pandas as pd
import certifi
from pymongo import MongoClient

# Load the dataset
file_path = '/Users/azeezmariam/pld8-db-assignment/Mongodb/car_purchasing.csv'
dataset = pd.read_csv(file_path, encoding='ISO-8859-1')

# Add a customer_id column, starting from 1
dataset['customer_id'] = range(1, len(dataset) + 1)

# Connect to MongoDB
client = MongoClient("MONGO_URL", tlsCAFile=certifi.where())
db = client['customer_data']  # Replace with your preferred database name
customers_collection = db['Customers']

