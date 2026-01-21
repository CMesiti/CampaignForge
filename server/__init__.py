from flask import Flask
import os
from dotenv import load_dotenv
from routes import userRoutes, campaignRoutes

#app factory, on import
def create_app(test_config = None):
    app = Flask(__name__)
    app.register_blueprint(userRoutes.users_bp)

    @app.route("/")
    def landing():
        return "Server is up and running"
    return app
