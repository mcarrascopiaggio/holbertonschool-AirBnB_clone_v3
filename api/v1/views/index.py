#!/usr/bin/python3
"""index pycode"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """return status"""
    stt = {"status": "OK"}
    return jsonify(stt)


@app_views.route('/stats')
def stats():
    """ endpoint that retrieves the number of each objects by type """
    Infor = {"amenities": storage.count(Amenity),
             "cities": storage.count(City),
             "places": storage.count(Place),
             "reviews": storage.count(Review),
             "states": storage.count(State),
             "users": storage.count(User), }
    return Infor
