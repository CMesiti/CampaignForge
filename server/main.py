from flask import Flask, jsonify, request, make_response
from config.db import get_connection
from models import Users, Campaigns, ModelBase, user_to_dict
from server import create_app
    
app = create_app() #use package
db = get_connection()
@app.route("/")
def landing():
    return "Server is up and running"


if __name__ == "__main__":
    ModelBase.metadata.create_all(db)
    app.run(debug=True)

