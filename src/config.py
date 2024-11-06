import os
from dotenv import load_dotenv
from supabase import create_client, Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.models import Base

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    raise ValueError("Supabase URL and API key must be set in environment variables.")

if SUPABASE_DB_URL:
    engine = create_engine(SUPABASE_DB_URL, echo=True) 
    Session = sessionmaker(bind=engine) 
    Base.metadata.create_all(engine)
else:
    raise ValueError("Supabase Database URL must be set in environment variables.")

def get_db():
    session = Session()
    try:
        yield session  
    finally:
        session.close() 
