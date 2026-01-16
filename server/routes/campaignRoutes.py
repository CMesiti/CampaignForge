from flask import request, jsonify, Flask, Blueprint
import requests
from controllers import campaignController


def add_campaign():
    new_campaign = campaignController.create_campaign()
    return new_campaign