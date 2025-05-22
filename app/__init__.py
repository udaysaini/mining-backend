from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS

import os

db = SQLAlchemy()


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    CORS(app)
    # CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    db.init_app(app)

    # Register the blueprints for the routes
    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # Regsister the error handlers
    from .errors import register_error_handlers

    register_error_handlers(app)

    return app
