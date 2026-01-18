from flask import Flask, jsonify, request, make_response
from config.db import get_connection
from sqlalchemy import text, select
from sqlalchemy.orm import Session, selectinload
from models import Users, Campaigns, ModelBase

# Refactor this into an app factory
# Add SQLAlchemy sessions properly
# Structure Campaign Forge for scaling (routes / blueprints)
# CORE vs ORM, The ORM uses sessions and Core uses a straight connection to the DBAPI
app = Flask(__name__)
db = get_connection()

@app.route("/")
def landing():
    return "Server is up and running"

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route("/users")
def get_users():
    result = {"Message":"", "Data":[]}
    try:
        with Session(db) as session:
            #this is a eager loading technique solving the N+1 Query problem
            stmt = select(Users).options(selectinload(Users.campaigns))
            #scalars returns list of objs and execute returns list of rows
            users_ls = session.scalars(stmt).all()
            # for user in users_ls:
            #     result["Data"].append(user.get_json())
        result["Message"] = "GET Successful"
        print(result)
        return jsonify({"Users":result["Message"]})

    except:
        result["Message"] = "GET ERROR"
        return jsonify({"ERROR":result})


@app.route("/users", methods=["POST"])
def register_user():
    result = {"Message":"", "Data":""}
    data = request.get_json()
    #Validate information

    #Assign and Commit New User
    #Add_all adds list of objects, commit method flushes pending transactions and commits to database.
    try:
        newUser = Users()
        with Session(db) as session:
            session.add(newUser)
            session.commit()
        result = "Query Successful"
    except:
        result["Message"] = "ADD ERROR"
    return jsonify(result)



@app.route("/users", methods = ["PUT"])
def update_user():
    pass   



@app.route("/users", methods=["DELETE"])
def remove_user():
    pass

#Lets try a different method. This endpoint will group operations together, 
@app.route("/campaigns", methods=["GET", "POST", "PUT", "DELETE"])
def campaign_dashboard():
    if request.method == "GET":
        with Session(db) as session:
            pass
    elif request.method == "POST":
        pass
    elif request.method == "PUT":
        pass
    else:
        pass



if __name__ == "__main__":
    ModelBase.metadata.create_all(db)
    app.run(debug=True)



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