from flask import request, jsonify, Flask, Blueprint
import requests
from controllers import campaignController
from flask import Flask, jsonify, request, make_response

campaigns_bp = Blueprint("campaigns", __name__, "/campaigns/v1/")
#Lets try a different method. This endpoint will group operations together, 
@campaigns_bp.route("/", methods=["GET", "POST", "PUT", "DELETE"])
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
