from server.config.db import init_db
from flask import Flask, jsonify
from flask_cors import CORS
from server.routes import userRoutes, campaignRoutes, authRoutes,playerCharRoutes
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from server.retrieval.chroma_db import init_vector_db
from server.retrieval.chat_model import init_llm

#app factory, on import
load_dotenv()
def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
    jwt = JWTManager(app)
    CORS(app) #security for requests
    #Since we use the g object we enable access to current app in configuration.
    with app.app_context():
        init_db(app)
        init_vector_db()
        # init_llm()

    app.register_blueprint(userRoutes.users_bp)
    app.register_blueprint(campaignRoutes.campaigns_bp)
    app.register_blueprint(authRoutes.auth_bp)
    app.register_blueprint(playerCharRoutes.pc_bp)
    return app


app = create_app()
@app.route("/status")
def check_status():
    return jsonify({"status":"API is Running!"}),200

if __name__ == "__main__":
    app.run(debug=True)

