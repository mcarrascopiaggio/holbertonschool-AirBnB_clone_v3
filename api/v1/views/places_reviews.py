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
