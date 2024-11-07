from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session 
from pydantic import BaseModel 
from src.config import supabase, get_db
from src.populate import populate_databases
from src.populate import populate_mongodb
from src.models import User  
from src.schemas import UserCreate, UserResponse 
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

#SQLAlchemy Models 
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    
SQLALCHEMY_DATABASE_URL = "your_database_url_here"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True

app = FastAPI()

@app.get("/")
def read_root(session: Session = Depends(get_db)):
    return {"Hello World"}

@app.post("/populate/postgres")
def populate_db(session: Session = Depends(get_db)):
    populate_databases(session)
    return {"message": "Database populated"}

@app.post("/populate/mongodb")
def populate_mongo():
    populate_mongodb()
    return {"message": "MongoDB populated"}

# CRUD Endpoints for PostgreSQL

# CREATE (POST)
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# READ (GET)
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# UPDATE (PUT)
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_user.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# DELETE (DELETE)
@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}