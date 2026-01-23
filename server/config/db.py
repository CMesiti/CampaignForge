from dotenv import load_dotenv
import os
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from models import ModelBase

#gives access to db.Models and db.Sessions
db = SQLAlchemy(model_class = ModelBase)
#Using flask sqlalchemy we initialize the extension on current application.
load_dotenv()
def init_db():
    print("Creating Connection Pool...")
    URL = os.getenv("DATABASE_URL")
    current_app.config["SQLALCHEMY_DATABASE_URI"] = URL
    db.init_app(current_app)
    db.create_all()


#Flask-sqlalchemy handles the engine object for us.
#The engine is not a connection, it is an object for the connection pool, telling how to create connection.
#The engine provides us with a connection object