from flask import Flask
from config.db import get_connection
from sqlalchemy import text

app = Flask(__name__)

@app.route("/")
def landing():
    return "Server is up and running"

@app.route("/users")
def get_users():
    result = "None"
    with db.begin() as connection:
        try:
            result = connection.execute(text("SELECT * FROM users"))
            print("Successful Query!")
        except:
            print("Query ERROR")
    
    return str(result)


if __name__ == "__main__":
    db = get_connection()
    app.run(debug=True)
    print("Closing Server")

