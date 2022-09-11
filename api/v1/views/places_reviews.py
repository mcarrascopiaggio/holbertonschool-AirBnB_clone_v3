#!/usr/bin/python3
"""
Create a new view for Review
object that handles all default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """
    Retrieves the list of all Review objects of a Place:
    GET /api/v1/places/<place_id>/reviews
    """
    list_all_reviews = []
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    for review in place.reviews:
        list_all_reviews.append(review.to_dict())

    return jsonify(list_review)


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_revieew(review_id):
    """Retrieves a Review object
    GET /api/v1/reviews/<review_id>"""
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)
