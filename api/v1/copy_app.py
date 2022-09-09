#!/usr/bin/python3
"""
Your first endpoint (route) will be to return the status of your API
line 3
line 4
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_session(self):
    """close session"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """error 404 page not found"""
    error = {"error": "Not found"}
    return (jsonify(error), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")

    if not host:
        host = "0.0.0.0"

    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
