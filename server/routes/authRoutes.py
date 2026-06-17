from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager, set_access_cookies, unset_jwt_cookies
from server.services.userService import UserService
from server.services.util import ServiceError
#Main ways for session authenticaiton:
#https://medium.com/@shubhamnalawade037/oauth2-vs-jwt-vs-sessions-developers-choose-wrong-3ff451375b43


#JWT for decoupled front-end and back-end, 
#Sessions with flask for standard monolithic applications with tightly coupled front-end and back-end.
#We will use JWT to allow for a more scalable approach, we will 
#Depends on SSR or CSR, server side rendering or client side. 

#We are follwing a CSR architecture, sending data leaving rendering work to the client.
#for SSR we would create HTML templates, fill, and render with each request.
auth_bp = Blueprint("auth", __name__, url_prefix="/auth/")

# store the token when you login, 
# and add the token as a header each time you make a request to a protected route. 
# Logging out is as simple as deleting the token.

@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    try:
        #401 errors for unauthorized
        #email and password
        data = request.get_json()
        #verify user
        service = UserService()
        user = service.login_user(data)
        #add additional info to JWT with add additional claims arg in create function
        access_token = create_access_token(identity = user.user_id)
        response = jsonify({"message":"Successfully Logged In"})
        set_access_cookies(response, access_token)
        return response
    except ServiceError as e:
        return jsonify({"ERROR":str(e)}), 401
    except Exception as e:
        return jsonify({"ERROR":"Internal server error "+str(e)}), 500