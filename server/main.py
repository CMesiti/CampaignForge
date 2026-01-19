from flask import Flask, jsonify, request, make_response
from config.db import get_connection
from sqlalchemy import text, select
from sqlalchemy.orm import Session, selectinload
from models import Users, Campaigns, ModelBase, user_to_dict
import bcrypt

def hash_pass(pswd):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(pswd, salt)
    return hash

def compare_pass(entered_pswd, hash):
    return bcrypt.checkpw(entered_pswd, hash)



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
    #401 errors for unauthorized
    pass


@app.route("/users")
def get_users():
    result = {"Users":[],"Message":""}
    try:
        with Session(db) as session:
            #this is a eager loading technique solving the N+1 Query problem
            stmt = select(Users).options(selectinload(Users.campaigns))
            #scalars returns list of objs and execute returns list of rows
            users_ls = session.scalars(stmt).all()
            for user in users_ls:
                result["Users"].append(user_to_dict(user))
        result["Message"] = "GET Successful"
        print(result)
        return jsonify({"Data":result}), 200
    except Exception as e:
        result["Message"] = f"GET ERROR, {e}"
        return jsonify({"ERROR":result})


@app.route("/users", methods=["POST"])
def register_user():
    result = {"Users":"","Message":""}
    data = request.get_json()
    #Validate information, **CHECK FOR DUPLICATES**
    try:
        if "email" not in data:
            result["Message"] = "Missing Email"
            return jsonify({"ERROR":result})
        if "password" not in data:
            result["Message"] = "Missing Password"
            return jsonify({"ERROR":result})
        if "display_name" not in data:
            data["display_name"] = data["email"].split('@')[0]

        #Assign and Commit New User
        with Session(db) as session:
            email_stmt = select(Users).where(Users.email == data["email"])
            email_scalar = session.scalars(email_stmt).one()
            if email_scalar:
                result["Message"] = "Email Taken"
                return jsonify({"ERROR":result}), 201
    
            newUser = Users()
            newUser.email =data["email"]
            pswd = hash_pass(data["password"])
            newUser.pass_hash = pswd
            newUser.display_name=data["display_name"]
            #Add_all adds list of objects, commit method flushes pending transactions and commits to database.
            session.add(newUser)
            session.commit()
            #after flush we assign server defaults to obj
            result["Users"] = user_to_dict(newUser)

        result["Message"] = "Created User Successfully"
        return jsonify({"Data": result})
    
    except Exception as e:
        result["Message"] = f"Register ERROR, {e}"
        return jsonify({"ERROR": result}), 400



@app.route("/users/<uuid:user_id>", methods = ["PUT"])
def update_user(user_id):
    #update the user by id
    #form is a dictionary
    pswd = request.form.get("password", None)
    display_name = request.form.get("display_name", None)
    if pswd:
        #add password constraints

        #hash and store
        pass

    elif display_name:
        pass
    else:
        return jsonify({"ERROR": "Missing Update Information"}), 400
  



@app.route("/users/<uuid:user_id>", methods=["DELETE"])
def remove_user(user_id):
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