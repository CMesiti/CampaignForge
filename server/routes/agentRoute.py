from flask import Blueprint, request, jsonify, Response
from server.retrieval.rulebook_assistant import get_agent_response
from flask_jwt_extended import jwt_required

agent_bp = Blueprint("agent", __name__, url_prefix="/agent/")

#Here we will create our blueprint and register the endpoint to interact with our RAG Agent.
@agent_bp.route("/query/<uuid:campaign_id>", methods=["GET", "POST"])
@jwt_required()
def agent_query_response(campaign_id):
    req_query = request.get_json()
    #move into retrieval folder
    user_query = req_query.get('user_query', None)
    if not user_query:
        return jsonify({"ERROR":
                        "Invalid request format "
                        "must be of the form - user_query: 'query'"}), 400
    try:
        return Response(get_agent_response(user_query, campaign_id))
        # response = get_agent_response(user_query, campaign_id)
        # return jsonify({"agent_response":response})
    except Exception as e:
        return jsonify({"ERROR": str(e)}), 500