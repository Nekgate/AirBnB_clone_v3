#!/usr/bin/python3
"""
create users
"""
from flask import jsonify, abort, request
from models.user import user
from models import Storage
from api.v1.views from app_views


@app_views.route('/user', strict_slashes=False)
def get_all_users():
    """
    Retrieving the users list
    """
    users = storage.all(User).values()
    return jsonify([User.to_dict() for User in users])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user():
    """
    Retrieving a single user
    """
    users = storage.get(User, User_id)
    if user:
        return jsonify(User.to_dict())
    else:
        return abort(404)


@app_views('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Delete a user object
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(User, user_id)
        storage.save()
        return jsonify(user.to_dict())
    else:
        aabort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    creating a user
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'email' not in data:
        return abort(400, 'Missing name')
    if 'passwoed' not in data:
        return abort(400, 'Missing password')

    user = User(**data)
    user.save()

    return jsonify(userr.to_dict()), 200


@app_views.route('/user/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    updating the user
    """
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            return abort(404, 'Not a JSON')
        if request.content_type != 'application/json':
            return abort(404, 'Not a JSON')
        data = request.get_json()

        ignore_keys = ['id', 'created_at', 'updated_at']

        for keys, value in data.items():
            if key not in ignore-keys:
                satattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        return abort(404)
