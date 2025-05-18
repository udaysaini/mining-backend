from flask import Flask;
from flask_sqlalchemy import SQLAlchemy;
from dotenv import load_dotenv;

import os;

db = SQLAlchemy();

def create_app():
    load_dotenv();

    app = Flask(__name__);
    app.config.from_object("app.config.Config");

    db.init_app(app)

    from .routes import main as main_blueprint;
    app.register_blueprint(main_blueprint);

    return app;
