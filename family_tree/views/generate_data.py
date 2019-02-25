from ..models import db, Person, Address
from flask import blueprints
from flask import jsonify
from faker import Faker

fake = Faker()
blueprint = blueprints.Blueprint('generate_data', __name__)

# for testing purposes only.
@blueprint.route('/generate_data', methods=['GET'])
def generate_data():
    db.drop_all()
    db.create_all()
    grandpa_1 = make_person()
    grandma_1 = make_person(last_name=grandpa_1.last_name)
    child_1 = make_person(last_name=grandpa_1.last_name, parents=[grandpa_1, grandma_1])

    grandpa_2 = make_person()
    grandma_2 = make_person(last_name=grandpa_2.last_name)
    child_2 = make_person(last_name=child_1.last_name, parents=[grandpa_2, grandma_2])
    
    grandchild_1 = make_person(last_name=child_1.last_name, parents=[child_1, child_2])
    grandchild_2 = make_person(last_name=child_1.last_name, parents=[child_1, child_2])
    
    db.session.commit()
    return jsonify('data created')


def make_person(last_name=None, addresses=None, parents=None):
    person = Person(
        first_name = fake.first_name(),
        last_name = last_name or fake.last_name(),
        phone_number = fake.phone_number(),
        email_address = fake.ascii_email(),
        birth_date = fake.past_date()
    )

    address = make_address()
    person.addresses.append(address)

    if parents:
        for parent in parents:
            person.parents.append(parent)

    db.session.add(person)
    return person


def make_address():
    address = Address(
        line_1 = fake.street_address(),
        city = fake.city(),
        state = fake.state(),
        zip_code = fake.postcode()
    )

    db.session.add(address)
    return address