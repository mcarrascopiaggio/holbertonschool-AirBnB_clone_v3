#!/usr/bin/python3
"""
Create a new view for Amenity objects that handles all default RESTFul AP
"""
from api.v1.views.states import all_states
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all Amenity objects: GET /api/v1/amenities"""
    all_amenities = storage.all(Amenity)
    list_amenities = []
    for amenitie in all_amenities.values():
        list_amenities.append(amenitie.to_dict())

    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id):
    """Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>"""
    amenitie = storage.get(Amenity, amenity_id)
    if amenitie:
        return jsonify(amenitie.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenitie(amenity_id):
    """
    deletes a Amenity object
    """
    amenitie = storage.get(Amenity, amenity_id)
    if amenitie is None:
        abort(404)
    else:
        storage.delete(amenitie)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenitie():
    """create state with request get json"""

    create_amenitie = request.get_json()
    if create_amenitie is None:
        abort(400, 'Not a JSON')
    if "name" not in create_amenitie:
        abort(400, 'Missing name')
    new_amenitie = Amenity(**create_amenitie)
    storage.new(new_amenitie)
    storage.save()
    return jsonify(new_amenitie.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_state(amenity_id):
    """Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>"""
    amenitie = storage.get(Amenity, amenity_id)
    if amenitie is None:
        abort(404)
    update_amenitie = request.get_json()
    if update_amenitie is None:
        abort(400, "Not a JSON")
    else:
        for key, value in update_amenitie.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(state, key, value)
            storage.save()
        return jsonify(amenitie.to_dict()), 200
