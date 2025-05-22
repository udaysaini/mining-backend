from flask import Blueprint, jsonify, request, abort
from app import db
from app.models.technician import Technician
from datetime import datetime, time
from app.utils.formatters import format_time_field, parse_time_string

# Create a blueprint for the technician routes
technician_bp = Blueprint("technicians", __name__, url_prefix="/technicians")


# Route to get all technicians
@technician_bp.route("", methods=["POST"])
def create_technician():
    print("POST Request: Create Technician")
    data = request.get_json()
    print("Data received:", data)

    # Validate required fields
    if not data or "name" not in data:
        abort(400, "Missing required fields: name")

    # Parse time strings and prevent SQLite errors
    available_from = parse_time_string(data.get("available_from"), "available_from")
    available_to = parse_time_string(data.get("available_to"), "available_to")

    # Create a new technician instance
    new_technician = Technician(
        name=data["name"],
        role=data.get("role"),
        skills=data.get("skills"),
        available_from=available_from,
        available_to=available_to,
    )

    # Add the new technician to the session and commit
    db.session.add(new_technician)
    db.session.commit()

    # Return a success message with the technician ID
    return (
        jsonify(
            {
                "message": "Technician created successfully",
                "technician_id": new_technician.id,
            }
        ),
        201,
    )


@technician_bp.route("", methods=["GET"])
def get_technicians():
    print("GET Request: All Technicians")
    # Get all technicians from the database
    technicians = Technician.query.all()

    # Convert the list of technicians to a list of dictionaries
    technicians_list = []
    for technician in technicians:
        formatted_available_from = format_time_field(
            technician.available_from, "available_from"
        )
        formatted_available_to = format_time_field(
            technician.available_to, "available_to"
        )

        technicians_list.append(
            {
                "id": technician.id,
                "name": technician.name,
                "role": technician.role,
                "skills": technician.skills,
                "available_from": formatted_available_from,
                "available_to": formatted_available_to,
            }
        )

    # Return the list of technicians as JSON
    return jsonify(technicians_list), 200


@technician_bp.route("/<int:technician_id>", methods=["GET"])
def get_technician(technician_id):
    print("GET Request : Technician ID:", technician_id)
    # get a specific technician by ID
    technician = Technician.query.get_or_404(
        technician_id, description=f"No technician found with id={technician_id}"
    )

    # technician = Technician.query.get(technician_id)
    # if not technician:
    #     abort(404, description=f"No technician found with id={technician_id}")

    # Format the available_from and available_to fields
    formatted_available_from = format_time_field(
        technician.available_from, "available_from"
    )
    formatted_available_to = format_time_field(technician.available_to, "available_to")

    # Convert the technician object to a dictionary
    technician_data = {
        "id": technician.id,
        "name": technician.name,
        "role": technician.role,
        "skills": technician.skills,
        "available_from": formatted_available_from,
        "available_to": formatted_available_to,
    }

    return jsonify(technician_data), 200


@technician_bp.route("/<int:technician_id>", methods=["PUT"])
def update_technician(technician_id):
    print("PUT Request : Technician ID:", technician_id)

    # fetch the technician by ID
    technician = Technician.query.get_or_404(
        technician_id, description=f"No technician found with id={technician_id}"
    )

    # Parse the request JSON
    data = request.get_json()
    if not data:
        abort(400, "No data provided for update")

    # Update the technician's attributes
    technician.name = data.get("name", technician.name)
    technician.role = data.get("role", technician.role)
    technician.skills = data.get("skills", technician.skills)
    technician.available_from = parse_time_string(
        data.get("available_from"), "available_from"
    )
    technician.available_to = parse_time_string(
        data.get("available_to"), "available_to"
    )

    # Validate the updated fields
    # if "name" not in data:
    #     abort(400, "No fields to update provided")

    # TODO: Should it be checking if name is in data?

    print("Data received for update:", data)

    # Update the technician's attributes based on the provided data
    if "name" in data:
        technician.name = data["name"]
    if "role" in data:
        technician.role = data["role"]
    if "skills" in data:
        technician.skills = data["skills"]

    if "available_from" in data:
        technician.available_from = parse_time_string(
            data["available_from"], "available_from"
        )
    if "available_to" in data:
        technician.available_to = parse_time_string(
            data["available_to"], "available_to"
        )

    # Commit the changes to the database
    db.session.commit()

    # Return a success message
    return jsonify({"message": "Technician updated successfully"}), 200


@technician_bp.route("/<int:technician_id>", methods=["DELETE"])
def delete_technician(technician_id):
    print("Delete Request: Technician ID:", technician_id)

    # Fetch the technician by ID
    technician = Technician.query.get_or_404(
        technician_id, description=f"No technician found with id={technician_id}"
    )

    # Delete the technician from the database
    db.session.delete(technician)
    db.session.commit()

    # Return a success message
    return jsonify({"message": "Technician deleted successfully"}), 204
