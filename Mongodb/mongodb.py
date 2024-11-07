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

# Loop through the dataset and insert each row as a document
for _, row in dataset.iterrows():
    customer_id = int(row['customer_id'])
    
    # Check if the customer already exists based on customer_id
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
        
        # Insert the document into the collection
        customers_collection.insert_one(customer_document)

print("Data insertion completed successfully.")
