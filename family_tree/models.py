from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

db = SQLAlchemy()

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_1 = db.Column(db.String)
    line_2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'line_1': self.line_1,
           'line_2': self.line_2,
           'city': self.city,
           'state': self.state,
           'zip_code': self.zip_code
       }
        

parent_to_child = db.Table('parent_to_child',
    db.Column('parent_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
    db.Column('child_id', db.Integer, db.ForeignKey('person.id'), primary_key=True)
)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    email_address = db.Column(db.String)
    addresses = db.relationship('Address', backref='person', lazy='dynamic')
    birth_date = db.Column(db.Date)
    parents = db.relationship('Person',
        secondary=parent_to_child,
        primaryjoin=(parent_to_child.c.parent_id == id),
        secondaryjoin=(parent_to_child.c.child_id == id),
        backref=db.backref('children', lazy='dynamic'),
        lazy='dynamic'
    )

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'first_name': self.first_name,
           'last_name': self.last_name,
           'phone_number': self.phone_number,
           'email_address': self.email_address,
           'birth_date': self.birth_date.strftime('%m/%d/%Y'),
           'addresses': [address.serialize for address in self.addresses] if self.addresses else None,
           'parents': [parent.id for parent in self.parents] if self.parents else None
       }
