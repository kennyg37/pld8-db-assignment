from mongoengine import Document, StringField, UUIDField, FloatField, IntField, ReferenceField
import uuid
from mongoengine import connect
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variable
MONGODB_URL = os.getenv("MONGODB_URL")

# Connect using the environment variable
connect(host=MONGODB_URL)

class User(Document):
    id = UUIDField(primary_key=True, default=uuid.uuid4, binary=False)
    name = StringField(required=True)
    email = StringField(required=True)
    

class Countries(Document):
    id = UUIDField(primary_key=True, default=uuid.uuid4, binary=False)
    country_name = StringField(required=True)


class UserData(Document):
    id = IntField(primary_key=True)
    user_id = ReferenceField(User, required=True)
    country_id = ReferenceField(Countries, required=True)
    gender = StringField()
    age = IntField()
    annual_salary = FloatField()
    credit_card = FloatField()
    net_worth = FloatField()
    car_purchase = FloatField()