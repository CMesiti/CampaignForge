from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from models import ModelBase

#This may need changes later, every connection request calls create_all()
load_dotenv()
def get_connection():
    print("Creating Database Connection")
    URL = os.getenv("DATABASE_URL")
    engine = create_engine(URL)
    # ModelBase.metadata.create_all(engine)
    #commit as you go architecture
    with engine.connect() as connection:
        print("Connection Successful")
    return engine