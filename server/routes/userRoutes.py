from flask import Blueprint, request, url_for, jsonify
from config.db import get_connection
from sqlalchemy import text, select, update, delete, insert
from sqlalchemy.orm import Session, selectinload
from models import Users, Campaigns, ModelBase, user_to_dict
from argon2 import PasswordHasher, exceptions
from flask import Flask, jsonify, request, make_response

db = get_connection()
#blueprint syntax, name, where it's defined, and url_prefix, versioning 1 of bp
users_bp = Blueprint("users", __name__, url_prefix = "/users/v1")

@users_bp.route("/")
def get_users():
    response = {"Users":[],"Message":""}
    try:
        with Session(db) as session:
            #this is a eager loading technique solving the N+1 Query problem
            stmt = select(Users).options(selectinload(Users.campaigns))
            #scalars returns list of objs and execute returns list of rows
            users_ls = session.scalars(stmt).all()
            for user in users_ls:
                response["Users"].append(user_to_dict(user))
        response["Message"] = "GET Successful"
        print(response)
        return jsonify({"Data":response}), 200
    

    except Exception as e:
        response["Message"] = f"GET ERROR, {e}"
        return jsonify({"ERROR":response}), 400
    
@users_bp.route("/", methods=["POST"])
def register_user():
    response = {"Users":"","Message":""}
    data = request.get_json()
    #Validate information, **CHECK FOR DUPLICATES**
    try:
        if "email" not in data:
            response["Message"] = "Missing Email"
            return jsonify({"ERROR":response})
        if "password" not in data:
            response["Message"] = "Missing Password"
            return jsonify({"ERROR":response})
        if "display_name" not in data:
            data["display_name"] = data["email"].split('@')[0]
        pswd = data["password"]
        email = data["email"]
        display_name = data["display_name"]
        #Assign and Commit New User
        with Session(db) as session:
            email_stmt = select(Users).where(Users.email == email)
            rows = session.scalars(email_stmt).first()
            print(rows)
            if rows:
                response["Message"] = "Email Taken"
                return jsonify({"ERROR":response}), 400
            if len(pswd) <= 12:
                return jsonify({"ERROR":"Password must be 12 or more chars"}), 400
            elif pswd.isalnum() or " " in pswd:
                return jsonify({"ERROR":"Must contain special character and no spaces"}), 400
            newUser = Users()
            newUser.email = email
            newUser.pass_hash = hash_pass(pswd)
            newUser.display_name = display_name
            #Add_all adds list of objects, commit method flushes pending transactions and commits to database.
            session.add(newUser)
            session.commit()
            #after flush we assign server defaults to obj
            response["Users"] = user_to_dict(newUser)
        response["Message"] = "Created User Successfully"
        return jsonify({"Data": response}), 201
    


    except Exception as e:
        response["Message"] = f"Register ERROR, {e}"
        return jsonify({"ERROR": response}), 400
    

@users_bp.route("/users/<uuid:user_id>", methods = ["PUT"])
def update_user(user_id):
    #form is a dictionary
    pswd = request.form.get("password", None)
    display_name = request.form.get("display_name", None)
    try:
        if pswd:
            #add password constraints
            if len(pswd) <= 12:
                return jsonify({"ERROR":"Password must be 12 or more chars"}), 400
            elif pswd.isalnum() or " " in pswd:
                return jsonify({"ERROR":"Must contain special character and no spaces"}), 400
            #hash and store
            hash = hash_pass(pswd)
            #get user
            with Session(db) as session:
                user = session.get(Users, user_id)
                user.pass_hash = hash
                session.commit()
            return jsonify({"Message": "Successfully updated password"}), 200
        elif display_name:
            if len(display_name) > 50:
                return jsonify({"ERROR":"Name must be less than 50 chars"}), 400
            elif " " in display_name:
                return jsonify({"ERROR":"No Spaces Allowed"}), 400
            with Session(db) as session:
                user = session.get(Users, user_id)
                user.display_name = display_name
                session.commit()
            return jsonify({"Message": "Successfully updated display name"}), 200
        else:
            return jsonify({"ERROR": "Missing Update Information"}), 400
        

    except Exception as e:
        return jsonify({"ERROR": e}), 400


@users_bp.route("/users/<uuid:user_id>", methods=["DELETE"])
def remove_user(user_id):
    pswd = request.form.get("password", None)
    try:
        with Session(db) as session:
            user = session.get(Users, user_id)
            if not pswd:
                return jsonify({"ERROR":"Password Required"}), 401
            is_valid, e = check_pass(pswd, user.pass_hash)
            if not is_valid:
                return jsonify({"ERROR":f"Validation Error {e}"}), 401
            session.delete(user)
            session.commit()
        return jsonify({"Message":"User Successfully deleted"}), 200
    

    except Exception as e:
        return jsonify({"ERROR": e}), 400
    #add session auth, ensure current user request, and recieve password
