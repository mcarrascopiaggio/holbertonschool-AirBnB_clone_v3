#!/usr/bin/python3
"""
Create a new view for Review
object that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from flask import abort
from flask import request


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def return_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    GET /api/v1/places/<place_id>/reviews
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def return_reviews_id(review_id):
    """
    Retrieves a Review object. : GET /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_id(review_id):
    """
    Deletes a Review object: DELETE /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object: PUT /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    update_r = request.get_json()
    if update_r is None:
        abort(400, "Not a JSON")
    else:
        for key, value in update_r.items():
            if key in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
                pass
            else:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """review create reviw aaaa"""

    reviews = request.get_json()

    if not storage.get("Place", place_id):
        abort(404)
    if not reviews:
        abort(400, 'Not a JSON')
    if "user_id" not in reviews:
        abort(400, 'Missing user_id')
    if not storage.get("User", reviews["user_id"]):
        abort(404)
    if "text" not in reviews:
        abort(400, "Missing text")

    reviews["place_id"] = place_id
    obj = Review(**reviews)
    storage.new(obj)
    storage.save()

    return (jsonify(obj.to_dict()), 201)
