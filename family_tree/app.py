from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from family_tree.models import db
import flask_cors, os

from family_tree.views import health_check, create_db, generate_data, people, relationships

cors = flask_cors.CORS()
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "family_tree.db"))
# db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    cors.init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    app.register_blueprint(health_check.blueprint, url_prefix='/api')
    app.register_blueprint(create_db.blueprint, url_prefix='/api')
    app.register_blueprint(generate_data.blueprint, url_prefix='/api')
    app.register_blueprint(people.blueprint, url_prefix='/api')
    app.register_blueprint(relationships.blueprint, url_prefix='/api')

    db.init_app(app)
    return app
