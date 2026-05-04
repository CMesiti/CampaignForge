from flask import Blueprint, request, jsonify
from server.services.userService import UserService
from server.services.util import ServiceError
from flask_jwt_extended import jwt_required
import logging, time
#blueprint syntax, name, where it's defined, and url_prefix, versioning 1 of bp
users_bp = Blueprint("users", __name__, url_prefix = "/v1/users/")

@users_bp.route("/")
def get_users():
    try:
        service = UserService()
        user_data = service.get_user_data()
        status_code = 200
        return jsonify({"user_data": user_data}), status_code
    except ServiceError as e:
        status_code = 400
        return jsonify({
            "ERROR":str(e)
            }), status_code
    except Exception as e:
        status_code = 500
        return jsonify({
            "ERROR":str(e)
            }), status_code


@users_bp.route("/", methods=["POST"])
def register_user():
    try:
        data = request.get_json()
        service = UserService()
        user_created = service.register_new_user(data)
        return jsonify({"user_data": user_created}), 201
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR": str(e)
            }), 500

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.   
@users_bp.route("/", methods = ["PUT"])
@jwt_required()
def update_user():
    #form is a dictionary, current user is user id in jwt
    try:
        data = request.get_json()
        service = UserService()
        user_updated = service.update_existing_user(data)
        return jsonify({"user_data": user_updated}), 200
    except ServiceError as e:
        return jsonify(
            {"ERROR": str(e)
             }), 400
    except Exception as e:
        return jsonify(
            {"ERROR": str(e)
             }), 500


@users_bp.route("/", methods=["DELETE"])
@jwt_required()
def remove_user():
    try:
        data = request.get_json()
        pswd = data.get("password", None)
        service = UserService()
        user_deleted = service.remove_existing_user(pswd)
        return jsonify({"user_data": user_deleted}), 204
    except ServiceError as e:
        return jsonify(
            {"ERROR": str(e)
             }), 400
    except Exception as e:
        return jsonify(
            {"ERROR": str(e)
             }), 500
    #add session auth, ensure current user request, and recieve password
