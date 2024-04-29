#!/usr/bin/python3
"""
View of places
"""
from flask import abort, jsonify, request
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    Retrieving places in a city
    """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    places = [places.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Returning a place object
    """
    place = storage.get(place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def delate_place(place_id):
    """
    Removing a place
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(Place)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/cities/<city_id>/places', metods=['POST'],
                 strict_slashe=False)
def create_place(city_id):
    """
    Creating a new place
    """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing user_id')

    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)
    data['city-id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views('/places/<place_id>', methods=[PUT], strict_slashes=False)
def update_place(place_id):
    """
    updating places with new features
    or new possibilities
    """
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'crated_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieving a place by simply searching
    Search by city_id and state_id
    to find a pace for user
    """
    if request.content_type != 'applicatio/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if data:
        states = data.get('states')
        cities = data.get('cities')
        amenities = data.get('amenities')
    if not (states or cities or amenities):
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)
    list_places = []

    if states:
        states_obj = [storage.get(state, state_id) for state_id in states]
        for state in states_obj:
            if states:
                for city in states.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, city_id) for city_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            all_places = storage.all(Place).values()
            amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
            for place in all_places:
                if all([am in place.amenities for am in amenities_obj]):
                    list_places.append(place)

    places = []
    for plc_obj in list_places:
        plc_dict = plc_obj.to_dict()
        plc_dict.pop('amenities', None)
        places.append(plc_dict)
    return jsonify(places)
                                                         
