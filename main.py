from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session  
from src.config import supabase, get_db
from src.populate import populate_databases

app = FastAPI()

@app.get("/")
def read_root(session: Session = Depends(get_db)):
    return {"Hello World"}

@app.post("/populate")
def populate_db(session: Session = Depends(get_db)):
    populate_databases(session)
    return {"message": "Database populated"}