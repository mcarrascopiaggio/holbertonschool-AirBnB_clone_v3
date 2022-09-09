#!/usr/bin/python3
"""init"""

# from api.v1.views.index import *
from flask import Flask, Blueprint

app = Flask(__name__)
app_views = Blueprint("app_views", __name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
