from flask import request, jsonify, Flask, Blueprint
from flask_jwt_extended import jwt_required
from server.services.campaignService import CampaignService
from server.services.util import ServiceError

campaigns_bp = Blueprint("campaigns", __name__, url_prefix="/v1/campaigns/")
#Lets try a different method. This endpoint will group operations together, 


#we can't group operations that require url parameters, also this makes it less readable
@campaigns_bp.route("/")
@jwt_required()
def get_user_campaigns():
    #get all campaings for that user
    #call user service, then use the JWT to get user id.
    #get campaigns using campaigns member associatation. 
    try:
        service = CampaignService()
        campaigns = service.get_campaigns()
        return jsonify({"campaign_data": campaigns}), 200
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":"Internal server error "+str(e)
            }), 500
    
@campaigns_bp.route("/create", methods=["POST"])
@jwt_required()
def create_campaign():
    #users creating are auto role 'DM'
    try:
        #form info - title, description
        data = request.get_json()
        service = CampaignService()
        campaign = service.create_new_campaign(data)
        return jsonify({"campaign_data": campaign}), 201
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":"Internal server error "+str(e)
            }), 500



@campaigns_bp.route("/enroll/<uuid:campaign_id>", methods=["POST"])
@jwt_required()
def join_campaign(campaign_id):
    #users joining are auto role 'player', Creator can copy paste campaign_id (like an invite code)
    try:
        service = CampaignService()
        service.enroll_user(campaign_id)
        return jsonify({"campaign_data": "Succesfully Enrolled"}), 201
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":"Internal server error "+str(e)
            }), 500


@campaigns_bp.route("/<uuid:campaign_id>", methods=["PUT"])
@jwt_required()
def update_campaign(campaign_id):
    try:
        data = request.get_json()
        service = CampaignService()
        updated_campaign = service.update_existing_campaign(data, campaign_id)
        return jsonify({"campaign_data":updated_campaign}), 200
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":"Internal server error "+str(e)
            }), 500

@campaigns_bp.route("/<uuid:campaign_id>/<uuid:user_id>")
@jwt_required()
def campaign_remove_user(campaign_id, user_id):
    try:
        service = CampaignService()
        service.remove_user
        return jsonify({"campaign_data": "Succesfully Removed User"}), 204
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":"Internal server error "+str(e)
            }), 500


@campaigns_bp.route("/<uuid:campaign_id>", methods=["DELETE"])
@jwt_required()
def delete_campaign(campaign_id):
    try:
        service = CampaignService()
        removed_campaign = service.delete_existing_campaign(campaign_id)
        return jsonify({"campaign_data": removed_campaign}), 204
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":"Internal server error "+str(e)
            }), 500
    
