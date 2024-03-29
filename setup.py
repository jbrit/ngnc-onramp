from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_cors import CORS
from flask_restful import abort
from flask_migrate import Migrate
from webargs.flaskparser import parser
from config import app_config
from views import api_blueprint, docs
from commands import command_blueprint
from models import db

# This error handler is necessary for usage with Flask-RESTful
# pylint: disable=unused-argument
@parser.error_handler
def handle_request_parsing_error(err, req, schema, **kwargs):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(422, errors=err.messages)


migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.update(app_config)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(command_blueprint)
    db.init_app(app)
    migrate.init_app(app, db)
    docs.init_app(app)
    CORS(app)
    return app
