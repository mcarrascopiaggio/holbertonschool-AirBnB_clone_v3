#!/usr/bin/python3
"""app pycode"""

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_session(self):
    """close session"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")

    if not host:
        host = "0.0.0.0"

    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
