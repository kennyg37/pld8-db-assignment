from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session  
from src.config import supabase, get_db
from src.populate import populate_databases
from src.populate import populate_mongodb

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

#CRUD Endpoints for PostgreSQL

# CREATE (POST)
@app.post("/users/", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# READ (GET)
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# UPDATE (PUT)
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User, db: Session = Depends(get_db)):
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