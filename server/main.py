from flask import Flask
from config.db import get_connection
from sqlalchemy import text

# Refactor this into an app factory
# Add SQLAlchemy sessions properly
# Structure Campaign Forge for scaling (routes / blueprints)
app = Flask(__name__)
db = get_connection()

@app.route("/")
def landing():
    return "Server is up and running"

@app.route("/users")
def get_users():
    result = "None"
    #begin once method
    with db.begin() as connection:
        try:
            result = connection.execute(text("SELECT * FROM users"))
            print("Successful Query!")
        except:
            print("Query ERROR")
    
    return str(result.fetchall())

@app.route("/campaigns")
def get_campaigns():
    results = "None"
    try:
        with db.begin() as connection:
            results = connection.execute(text("SELECT * FROM campaigns"))
            print("Successful Query!")
    except:
        print("Query Error")
    return str(results.fetchall())



if __name__ == "__main__":
    app.run(debug=True)
    print("Closing Server")

