#!/usr/bin/python3
"""
Create a new view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    all_states = storage.all(State)
    list_states = []
    for state in all_states.values():
        list_states.append(state.to_dict())

    return jsonify(list_states)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_states(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
"""
deletes a State object
"""
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	else:
		storage.delete(state)
		storage.save()
	return jsonify({}), 200
"""
De aca saque lo de ese return que no tengo muy claro si va a funcionar
https://stackoverflow.com/questions/45412228/sending-json-and-status-code-with-a-flask-response
"""

"""
@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    return 


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
"""
