#!/usr/bin/python3
"""
User instance
"""


from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all Place objects of a City
    GET /api/v1/cities/<city_id>/places"""
    list_places = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    places = storage.all("Place")
    for place in places.values():
        if place.city_id == city_id:
            list_places.append(place.to_dict())

    return jsonify(list_places)


@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object. : GET /api/v1/places/<place_id>"""
    theplace = storage.get("Place", place_id)
    if theplace is None:
        abort(404)
    else:
        return jsonify(theplace.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    deletes a Place object
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a City instance"""
    body = request.get_json()
    user_id = body.get("user_id")

    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in body.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)
    elif "user_id" not in body.keys():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    place = Place(**body)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """Updates a Place object: PUT /api/v1/places/<place_id>"""
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    update_places = request.get_json()
    if update_places is None:
        abort(400, "Not a JSON")
    else:
        for key, value in update_places.items():
            if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(places, key, value)
        storage.save()
        return jsonify(places.to_dict()), 200
