from flask import Blueprint
from flask_apispec import FlaskApiSpec
from flask_restful import Api

from resources import RedirectSwagger, Wallet, Webhook

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

# API routes -- start
api.add_resource(Wallet, "/<address>")
api.add_resource(Webhook, "/")
api.add_resource(RedirectSwagger, "/")
# API routes -- end


docs = FlaskApiSpec()

# API docs -- start
docs.register(Wallet, blueprint="api")
docs.register(Webhook, blueprint="api")
docs.register(RedirectSwagger, blueprint="api")
# API docs -- end