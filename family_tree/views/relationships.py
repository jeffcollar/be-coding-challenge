from flask import blueprints, jsonify, abort
from ..models import Person

blueprint = blueprints.Blueprint('relationships', __name__)

@blueprint.route('/siblings/<id>', methods=['GET'])
def get_siblings(id):
    person = Person.query.get(id)
    if person:
        parent_ids = [parent.id for parent in person.parents]
        siblings = Person.query.filter(Person.parents.any(Person.id.in_(parent_ids)), Person.id != person.id)
        return jsonify(siblings = [person.serialize for person in siblings])
    else:
        abort(404)

@blueprint.route('/parents/<id>', methods=['GET'])
def get_parents(id):
    person = Person.query.get(id)
    if person:
        parents = Person.query.get(id).parents
        return jsonify(parents = [person.serialize for person in parents])
    else:
        abort(404)

@blueprint.route('/children/<id>', methods=['GET'])
def get_children(id):
    person = Person.query.get(id)
    if person:
        children = Person.query.filter(Person.parents.any(Person.id==id))
        return jsonify(children = [child.serialize for child in children])
    else:
        abort(404)

@blueprint.route('/grandparents/<id>', methods=['GET'])
def get_grandparents(id):
    person = Person.query.get(id)
    if person:
        parent_ids = [parent.id for parent in person.parents]
        grandparents = Person.query.filter(Person.children.any(Person.id.in_(parent_ids)))
        return jsonify(grandparents = [person.serialize for person in grandparents])
    else:
        abort(404)

# For a given person list all of their siblings
# - For a given person list all of their parents
# - For a given person list all their children
# - For a given person list all of their grandparents