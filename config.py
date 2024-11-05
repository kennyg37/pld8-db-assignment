import os
from dotenv import load_dotenv
from supabase import create_client, Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

# Create Supabase client
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    raise ValueError("Supabase URL and API key must be set in environment variables.")

# Create the SQLAlchemy engine and session
if SUPABASE_DB_URL:
    engine = create_engine(SUPABASE_DB_URL, echo=True)  # Use synchronous engine
    Session = sessionmaker(bind=engine)  # Create a session factory
else:
    raise ValueError("Supabase Database URL must be set in environment variables.")

# Dependency to get a database session
def get_db():
    session = Session()  # Create a new session
    try:
        yield session  # Yield the session to be used
    finally:
        session.close()  # Close the session after use
