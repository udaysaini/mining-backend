# Equipment routes for Flask application
# This module defines the routes for managing equipment in the application.
from flask import Blueprint, request, jsonify, abort
from app import db
from app.models.equipment import Equipment
from app.models.technician import Technician
from datetime import datetime, time
from app.utils.formatters import format_time_field, parse_time_string

# Create a blueprint for the equipment routes
equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipment")


# Route to create a new equipment item
@equipment_bp.route("", methods=["POST"])
def create_equipment():
    print("POST Request: Create Equipment")
    data = request.get_json()
    print("Data received:", data)

    # Validate required fields
    if not data or "name" not in data:
        abort(400, "Missing required fields: name")

    # Parse time strings and prevent SQLite errors
    available_from = parse_time_string(data.get("available_from"), "available_from")
    available_to = parse_time_string(data.get("available_to"), "available_to")

    # Create a new equipment instance
    new_equipment = Equipment(
        name=data["name"],
        type=data.get("type"),
        status=data.get("status"),
        available_from=available_from,
        available_to=available_to,
    )

    # Add the new equipment to the session and commit
    db.session.add(new_equipment)
    db.session.commit()

    # Return a success message with the equipment ID
    return (
        jsonify(
            {
                "message": "Equipment created successfully",
                "equipment_id": new_equipment.id,
            }
        ),
        201,
    )


# Route to get all equipment items
@equipment_bp.route("", methods=["GET"])
def get_all_equipment():
    print("GET Request: Get All Equipment")
    equipment_list = Equipment.query.all()
    print("Equipment found:", equipment_list)

    # Format the equipment data for the response
    formatted_equipment = [
        {
            "id": equip.id,
            "name": equip.name,
            "type": equip.type,
            "status": equip.status,
            "available_from": format_time_field(equip.available_from),
            "available_to": format_time_field(equip.available_to),
        }
        for equip in equipment_list
    ]

    return jsonify(formatted_equipment), 200


# Route to get a specific equipment item by ID
@equipment_bp.route("/<int:equipment_id>", methods=["GET"])
def get_equipment_by_id(equipment_id):
    print(f"GET Request: Get Equipment by ID {equipment_id}")
    equipment = Equipment.query.get(equipment_id)

    if not equipment:
        abort(404, "Equipment not found")

    # Format the equipment data for the response
    formatted_equipment = {
        "id": equipment.id,
        "name": equipment.name,
        "type": equipment.type,
        "status": equipment.status,
        "available_from": format_time_field(equipment.available_from),
        "available_to": format_time_field(equipment.available_to),
    }

    return jsonify(formatted_equipment), 200


# Route to update an existing equipment item
@equipment_bp.route("/<int:equipment_id>", methods=["PUT"])
def update_equipment(equipment_id):
    print(f"PUT Request: Update Equipment ID {equipment_id}")
    data = request.get_json()
    print("Data received:", data)

    # Validate required fields
    if not data or "name" not in data:
        abort(400, "Missing required fields: name")

    # Find the equipment item to update
    equipment = Equipment.query.get(equipment_id)
    if not equipment:
        abort(404, "Equipment not found")

    # Update the equipment item with new data
    equipment.name = data["name"]
    equipment.type = data.get("type")
    equipment.status = data.get("status")
    equipment.available_from = parse_time_string(
        data.get("available_from"), "available_from"
    )
    equipment.available_to = parse_time_string(data.get("available_to"), "available_to")

    # Commit the changes to the database
    db.session.commit()

    return jsonify({"message": "Equipment updated successfully"}), 200


# Route to delete an equipment item
@equipment_bp.route("/<int:equipment_id>", methods=["DELETE"])
def delete_equipment(equipment_id):
    print(f"DELETE Request: Delete Equipment ID {equipment_id}")
    equipment = Equipment.query.get(equipment_id)

    if not equipment:
        abort(404, "Equipment not found")

    # Delete the equipment item from the database
    db.session.delete(equipment)
    db.session.commit()

    return jsonify({"message": "Equipment deleted successfully"}), 200


# Route to assign equipment to a technician
@equipment_bp.route("/<int:equipment_id>/assign/<int:technician_id>", methods=["POST"])
def assign_equipment_to_technician(equipment_id, technician_id):
    print(
        f"POST Request: Assign Equipment ID {equipment_id} to Technician ID {technician_id}"
    )
    equipment = Equipment.query.get(equipment_id)
    technician = Technician.query.get(technician_id)

    if not equipment:
        abort(404, "Equipment not found")
    if not technician:
        abort(404, "Technician not found")

    # Assign the equipment to the technician
    equipment.assigned_to = technician.id
    db.session.commit()

    return jsonify({"message": "Equipment assigned successfully"}), 200


# Route to unassign equipment from a technician
@equipment_bp.route("/<int:equipment_id>/unassign", methods=["POST"])
def unassign_equipment_from_technician(equipment_id):
    print(f"POST Request: Unassign Equipment ID {equipment_id}")
    equipment = Equipment.query.get(equipment_id)

    if not equipment:
        abort(404, "Equipment not found")

    # Unassign the equipment from the technician
    equipment.assigned_to = None
    db.session.commit()

    return jsonify({"message": "Equipment unassigned successfully"}), 200


# Route to get all equipment assigned to a technician
@equipment_bp.route("/technician/<int:technician_id>", methods=["GET"])
def get_equipment_by_technician(technician_id):
    print(f"GET Request: Get Equipment assigned to Technician ID {technician_id}")
    equipment_list = Equipment.query.filter_by(assigned_to=technician_id).all()

    # Format the equipment data for the response
    formatted_equipment = [
        {
            "id": equip.id,
            "name": equip.name,
            "type": equip.type,
            "status": equip.status,
            "available_from": format_time_field(equip.available_from, "available_from"),
            "available_to": format_time_field(equip.available_to, "available_to"),
        }
        for equip in equipment_list
    ]

    return jsonify(formatted_equipment), 200
