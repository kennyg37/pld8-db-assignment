from mongoengine import connect
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

client = AsyncIOMotorClient(MONGODB_URL, tls=True, tlsAllowInvalidCertificates=True)

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