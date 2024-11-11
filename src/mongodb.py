import os
from dotenv import load_dotenv
import pandas as pd
import certifi
from pymongo import MongoClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# Load the dataset
file_path = 'C:/Users/HP/Desktop/pld8-db-assignment/data/car_purchasing.csv'
dataset = pd.read_csv(file_path, encoding='ISO-8859-1')
dataset = dataset.head(50)

# Add a customer_id column
dataset['customer_id'] = range(1, len(dataset) + 1)

# Connect to MongoDB
client = MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
db = client['customer_data']

# Collections
customers_collection = db['Customers']
contacts_collection = db['Contacts']
financial_info_collection = db['FinancialInfo']

# Insert data into collections
for _, row in dataset.iterrows():
    customer_id = int(row['customer_id'])
    
    # Insert into Customers collection
    if not customers_collection.find_one({"customer_id": customer_id}):
        customer_document = {
            "customer_id": customer_id,
            "name": row['customer name'],
            "demographics": {
                "gender": row['gender'],
                "age": row['age']
            }
        }
        customers_collection.insert_one(customer_document)

    # Insert into Contacts collection
    if not contacts_collection.find_one({"customer_id": customer_id}):
        contact_document = {
            "customer_id": customer_id,
            "email": row['customer e-mail'],
            "country": row['country']
        }
        contacts_collection.insert_one(contact_document)
    
    # Insert into FinancialInfo collection
    if not financial_info_collection.find_one({"customer_id": customer_id}):
        financial_document = {
            "customer_id": customer_id,
            "annual_salary": row['annual Salary'],
            "credit_card_debt": row['credit card debt'],
            "net_worth": row['net worth'],
            "car_purchase_amount": row['car purchase amount']
        }
        financial_info_collection.insert_one(financial_document)

print("Data insertion into all collections completed successfully.")