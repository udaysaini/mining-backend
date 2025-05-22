from flask import Blueprint
from .technician_routes import technician_bp
from .equipment_routes import equipment_bp
from .shift_routes import shift_bp

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return {"message": "Hello, World! This is the home page."}


@main.route("/about")
def about():
    return {"message": "This is the about page."}


# Regsiter the blueprints
main.register_blueprint(technician_bp)
main.register_blueprint(equipment_bp)
main.register_blueprint(shift_bp)
