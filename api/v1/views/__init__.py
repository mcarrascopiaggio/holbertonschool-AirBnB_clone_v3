#/usr/bin/python3
"""init"""

from flask import Flask, Blueprint

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")

from api.v1.views.index import *
