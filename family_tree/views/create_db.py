from flask import blueprints
from flask import jsonify
from ..models import db

blueprint = blueprints.Blueprint('create_db', __name__)

# for testing purposes only.
@blueprint.route('/create_db', methods=['GET'])
def create_db():
    db.drop_all()
    db.create_all()
    return jsonify('database created')
