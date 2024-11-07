from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGODB_URL = os.getenv("mongodb+srv://eddy:eddy1234@cluster0.bry6h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Connect to MongoDB
client = MongoClient(MONGODB_URL)
db = client["your_database_name"]  # Replace with your MongoDB database name
user_collection = db["users"]      # Replace with the name of your collection

app = FastAPI()

# Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(UserCreate):
    id: str  # MongoDB ObjectId as a string

    class Config:
        orm_mode = True


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/populate/mongodb")
def populate_mongo():
    # Call your MongoDB population function here
    populate_mongodb()
    return {"message": "MongoDB populated"}

# CRUD Endpoints for MongoDB

# CREATE (POST)
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    user_data = user.dict()
    result = user_collection.insert_one(user_data)
    user_data["id"] = str(result.inserted_id)
    return user_data

# READ (GET)
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    return user

# UPDATE (PUT)
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, updated_user: UserCreate):
    update_data = {"$set": updated_user.dict()}
    result = user_collection.update_one({"_id": ObjectId(user_id)}, update_data)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    user["id"] = str(user["_id"])
    return user

# DELETE (DELETE)
@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: str):
    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
