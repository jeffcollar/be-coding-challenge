from flask import blueprints, jsonify, abort
from ..models import Person

blueprint = blueprints.Blueprint('people', __name__)

@blueprint.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    return jsonify(people = [person.serialize for person in people])

@blueprint.route('/people/<id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)
    if person:
        return jsonify(person.serialize)
    else:
        abort(404)
