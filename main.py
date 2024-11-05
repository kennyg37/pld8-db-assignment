from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session  # Change this to import the synchronous Session
from config import supabase, get_db  # Ensure you import the correct get_db function

app = FastAPI()

@app.get("/")
def read_root(session: Session = Depends(get_db)):  # Use Session instead of AsyncSession
    return {"Hello World"}