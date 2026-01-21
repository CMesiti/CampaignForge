from flask import Flask, Blueprint


auth_bp = Blueprint("auth", __name__, url_prefix="/auth/")


@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    #401 errors for unauthorized
    pass

