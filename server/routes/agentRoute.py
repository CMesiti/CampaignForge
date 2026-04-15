from flask import Blueprint, request, jsonify
from retrieval.rulebook_assistant import get_agent_response

agent_bp = Blueprint("agent", __name__, url_prefix="/agent/")

#Here we will create our blueprint and register the endpoint to interact with our RAG Agent.
@agent_bp.route('/query', methods=["GET", "POST"])
def agent_query_response():
    req_query = request.get_json()

    #move into retrieval folder
    user_query = req_query.get('user_query', None)
    if not user_query:
        return jsonify({"ERROR":
                        "Invalid request format "
                        "must be of the form - user_query: 'query'"}), 400
        
    return ""