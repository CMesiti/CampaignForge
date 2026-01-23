from flask import Blueprint, request, jsonify
from models import Users
from services.userService import UserService, ServiceError

#blueprint syntax, name, where it's defined, and url_prefix, versioning 1 of bp
users_bp = Blueprint("users", __name__, url_prefix = "/users/v1")

@users_bp.route("/")
def get_users():
    try:
        service = UserService()
        user_data = service.get_user_data()
        return jsonify({
            "Data": user_data
            }), 200
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":str(e)
            }), 500


@users_bp.route("/", methods=["POST"])
def register_user():
    data = request.get_json()
    #Validate information, **CHECK FOR DUPLICATES**
    try:
        service = UserService()
        user_created = service.register_new_user(data)
        return jsonify({
            "user_data": user_created
            }), 201
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR": str(e)
            }), 500
    

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
