from flask import request, jsonify, Flask
import requests
from controllers import campaignController

def add_campaign():
    data = request.get_json()
    new_campaign = campaignController.create_campaign()
    return new_campaign