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


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """create place post"""

    places = request.get_json()

    cities = storage.get("City", city_id)
    if cities:
        if not places:
            abort(400, 'Not a JSON')
        if "user_id" not in places:
            abort(400, "Missing user_id")
        if not storage.get("User", places["user_id"]):
            abort(404)
        if "name" not in places:
            abort(400, 'Missing name')

        places["city_id"] = city_id
        obj = Place(**places)
        storage.new(obj)
        storage.save()

        return (jsonify(obj.to_dict()), 201)
    abort(404)
