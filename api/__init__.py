import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from werkzeug.exceptions import HTTPException

ma = Marshmallow()
load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "db.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Serialization
    ma.init_app(app)

    # Blueprints
    from api.routes import forecast_routes, file_routes

    app.register_blueprint(forecast_routes.bp)
    app.register_blueprint(file_routes.bp)

    # Error handling
    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        return (
            jsonify(
                {
                    "code": err.code,
                    "name": err.name,
                    "description": err.description,
                }
            ),
            err.code,
        )

    return app
