from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import ModelBase

load_dotenv()
def get_connection():
    URL = os.getenv("DATABASE_URL")
    engine = create_engine(URL)
    ModelBase.metadata.create_all(engine)
    #commit as you go architecture
    with engine.connect() as connection:
        print("Connection Successful")
    return engine