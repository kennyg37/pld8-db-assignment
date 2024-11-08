import os
from dotenv import load_dotenv
import pandas as pd
import certifi
from pymongo import MongoClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

file_path = 'C:/Users/USER/Desktop/ken/Alu/fastapi/pld8-db-assignment/data/car_purchasing.csv'
dataset = pd.read_csv(file_path, encoding='ISO-8859-1')
dataset = dataset.head(10)

dataset['customer_id'] = range(1, len(dataset) + 1)

client = MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
db = client['customer_data']  
customers_collection = db['Customers']

for _, row in dataset.iterrows():
    customer_id = int(row['customer_id'])
    
    existing_customer = customers_collection.find_one({"customer_id": customer_id})
    
    if existing_customer:
        print(f"Customer with customer_id {customer_id} already exists, skipping insertion.")
    else:
        customer_document = {
            "customer_id": customer_id,
            "name": row['customer name'],
            "contact_info": {
                "email": row['customer e-mail'],
                "country": row['country']
            },
            "demographics": {
                "gender": row['gender'],
                "age": row['age']
            },
            "financial_info": {
                "annual_salary": row['annual Salary'],
                "credit_card_debt": row['credit card debt'],
                "net_worth": row['net worth'],
                "car_purchase_amount": row['car purchase amount']
            }
        }
        
        customers_collection.insert_one(customer_document)

print("Data insertion completed successfully.")
