import os

from flask import Flask
from flask_marshmallow import Marshmallow

ma = Marshmallow()


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
    from api.routes import forecast_routes

    app.register_blueprint(forecast_routes.bp)

    # Error handling
    # TODO: Implement error handling

    return app
