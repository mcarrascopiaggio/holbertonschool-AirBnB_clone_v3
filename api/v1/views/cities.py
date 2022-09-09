#!/usr/bin/python3
"""
new view for City objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def all_states_city():
    """Retrieves the list of all City objects of a State.
    GET /api/v1/states/<state_id>/cities"""
    list_cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities():
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_cities(city_id):
    """Retrieves the list of all City objects of a State.
    GET /api/v1/states/<state_id>/cities"""
    cities = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """
    deletes a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route("states/<state_id>/cities",
                 methods=["POST"],
                 strict_slashes=False)
def post_city(city_id):
    """Creates a City: POST /api/v1/states/<state_id>/cities"""

    state = storage.get(State, state_id)
    if state is None:
        abort(400)

    create_city = request.get_json()
    if create_city is None:
        abort(400, "Not a JSON")
    if "name" not in create_city:
        abort(400, 'Missing name')
    new_city = City(**create_city)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """Updates a City object: PUT /api/v1/cities/<city_id>"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    update_city = request.get_json()
    if update_city is None:
        abort(400, "Not a JSON")
    else:
        for key, value in update_city.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(state, key, value)
            storage.save()
        return jsonify(city.to_dict()), 200
