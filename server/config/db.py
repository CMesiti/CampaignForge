from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

def get_connection():
    URL = os.getenv("DATABASE_URL")
    engine = create_engine(URL)
    with engine.connect() as connection:
        print("Connection Successful")
    return engine