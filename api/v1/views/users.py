#!/usr/bin/python3
"""
Create a new view for State objects that handles all default RESTFul API
"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves the list of all User objects: GET /api/v1/users"""
    all_users = storage.all(User)
    list_users = []
    for user in all_users.values():
        list_users.append(user.to_dict())

    return jsonify(list_users)


@app_views.route('/users/<string:user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_users(user_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    deletes a user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """create state with re	quest get json"""

    create_user = request.get_json()
    if create_user is None:
        abort(400, 'Not a JSON')
    if "email" not in create_user:
        abort(400, 'Missing email')
    if "email" not in create_user:
        abort(400, 'Missing password')

    new_user = User(**create_user)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    update_user = request.get_json()
    if update_user is None:
        abort(400, "Not a JSON")
    else:
        for key, value in update_user.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(user, key, value)
            storage.save()
        return jsonify(user.to_dict()), 200
