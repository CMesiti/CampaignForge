from server.config.db import init_db
from server.config.logging_config import init_logging
from flask import Flask, jsonify, g, request
from flask_cors import CORS
from server.routes import agentRoute, userRoutes, campaignRoutes, authRoutes,playerCharRoutes
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os, time, logging
from server.retrieval.chroma_db import init_vector_db
from server.retrieval.chat_model import init_llm
from server.retrieval.rulebook_assistant import init_agent

#app factory, on import
load_dotenv()
logger = logging.getLogger(__name__)
def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    init_logging()
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
    jwt = JWTManager(app)
    CORS(app) #security for requests
    #Since we use the g object we enable access to current app in configuration.
    with app.app_context():
        init_db(app)
        with_rag = input("Run with RAG init? (y/n): ").strip().lower()
        if with_rag == 'y':
            init_vector_db()
            init_llm()
            init_agent()
    app.register_blueprint(agentRoute.agent_bp)
    app.register_blueprint(userRoutes.users_bp)
    app.register_blueprint(campaignRoutes.campaigns_bp)
    app.register_blueprint(authRoutes.auth_bp)
    app.register_blueprint(playerCharRoutes.pc_bp)

    @app.before_request
    def start_req():
        g.req_time = time.perf_counter()

    @app.after_request
    def log_request(response):
        exec_time = int((time.perf_counter() - g.req_time)*1000)
        logger.info(f'{request.method} - {exec_time}ms - {response.status_code}')
        return response
    

    return app

app = create_app()
@app.route("/status")
def check_status():
    return jsonify({"status":"API is Running!"}),200

if __name__ == "__main__":
    app.run(debug=True)

