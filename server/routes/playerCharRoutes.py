from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from server.services.util import ServiceError
from server.services.playerCharService import PlayerService

pc_bp = Blueprint("pc_bp", __name__, url_prefix="/v1/player-characters/")

#each player character action is related to a specific campaign

@pc_bp.route("/<uuid:campaign_id>")
def get_player_characters(campaign_id):
    try:
        service = PlayerService()
        campaign_players = service.get_campaign_players(campaign_id)
        return jsonify({"player_data": campaign_players}), 200
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":"Internal server error "+str(e)
            }), 500


@pc_bp.route("/<uuid:campaign_id>", methods=["POST"])
@jwt_required()
def create_player_character(campaign_id):
    try:
        player_data = request.get_json()
        service = PlayerService()
        player = service.create_new_player(player_data, campaign_id)
        return jsonify({"player_data":player}), 201
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":"Internal server error "+str(e)
            }), 500
    

@pc_bp.route("/<uuid:character_id>", methods=["PUT"])
@jwt_required()
def update_player_character(character_id):
    try:
        updates = request.get_json()
        service = PlayerService()
        player = service.update_existing_player(updates, character_id)
        return jsonify({"player_data":player}), 200
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":"Internal server error "+str(e)
            }), 500
    


@pc_bp.route("/<uuid:character_id>", methods=["DELETE"])
@jwt_required()
def delete_player_character(character_id):
    try:
        service = PlayerService()
        service.delete_existing_player(character_id)
        return jsonify({"player_data": "successfully deleted"}), 204
    except ServiceError as e:
        return jsonify({
            "ERROR":str(e)
            }), 400
    except Exception as e:
        return jsonify({
            "ERROR":"Internal server error "+str(e)
            }), 500


#create, update, get, and delete player characters