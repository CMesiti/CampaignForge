from flask import Flask, jsonify
from config.db import get_connection
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from models import Users, Campaigns

# Refactor this into an app factory
# Add SQLAlchemy sessions properly
# Structure Campaign Forge for scaling (routes / blueprints)

# CORE vs ORM, The ORM uses sessions and Core uses a straight connection to the DBAPI
app = Flask(__name__)
db = get_connection()

@app.route("/")
def landing():
    return "Server is up and running"

# @app.route("/users")
# def get_users():
#     result = "None"
#     #begin once method
#     with db.begin() as connection:
#         try:
#             result = connection.execute(text("SELECT * FROM users"))
#             print("Successful Query!")
#         except:
#             print("Query ERROR")
    
#     return str(result.fetchall())

# @app.route("/campaigns")
# def get_campaigns():
#     results = "None"
#     try:
#         with db.begin() as connection:
#             results = connection.execute(text("SELECT * FROM campaigns"))
#             print("Successful Query!")
#     except:
#         print("Query Error")
#     return str(results.fetchall())


@app.route("/users")
def get_users():
    result = "None"
    try:
        with Session(db) as session:
            stmt = select(Users)
            #scalars returns list of objs and execute returns list of rows
            user_obj = session.scalars(stmt).all()
        result = str(user_obj)
    except:
        result = "Get Query Error"
    return result



@app.route("/users", methods=["POST"])
def add_user():
    result = "None"
    try:
        newUser = Users()
        newUser.email = "example@example.com"
        newUser.display_name = "tester"
        newUser.pass_hash = "mypass123"
        with Session(db) as session:
            session.add(newUser)
            session.commit()
        result = "Query Successful"
    except:
        result = "Insert Query Error"
    return result
        


if __name__ == "__main__":
    app.run(debug=True)


