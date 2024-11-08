from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# MongoDB URI encoding
password = os.getenv("MONGO_PASSWORD")
encoded_password = quote_plus(password)

# MongoDB connection using motor for async operations
client = AsyncIOMotorClient(
    f"mongodb+srv://mazeez:{encoded_password}@cluster0.bsxpc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    tls=True,
    tlsAllowInvalidCertificates=True
)

# Select the database and collection
db = client['customer_data']
customers_collection = db['Customers']

# Pydantic models for validation
class ContactInfo(BaseModel):
    email: str
    country: str

class Demographics(BaseModel):
    gender: int
    age: float

class FinancialInfo(BaseModel):
    annual_salary: float
    credit_card_debt: float
    net_worth: float
    car_purchase_amount: float

class Customer(BaseModel):
    customer_id: int
    name: str
    contact_info: ContactInfo
    demographics: Demographics
    financial_info: FinancialInfo

# FastAPI instance
app = FastAPI()

@app.post("/customers/", response_model=dict)
async def create_customer(customer: Customer):
    # Check if the customer_id already exists in the database
    existing_customer = await customers_collection.find_one({"customer_id": customer.customer_id})
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer ID already exists")

    # If customer_id is unique, insert the customer
    customer_data = customer.dict()
    result = await customers_collection.insert_one(customer_data)
    return {"id": str(result.inserted_id)}

@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    # Fetch customer by customer_id
    customer = await customers_collection.find_one({"customer_id": customer_id})
    if not customer:
        print(f"Customer not found in database for customer_id: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")

    # Convert _id to string for easier readability
    customer["_id"] = str(customer["_id"])
    return customer

