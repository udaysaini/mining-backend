from flask import Blueprint, request, jsonify, abort
from app import db
from app.models.shift import Shift
from app.models.technician import Technician
from app.models.equipment import Equipment
from datetime import datetime
from app.utils.formatters import (
    parse_time_string,
    format_time_field,
    parse_date_string,
    format_date_field,
)

shift_bp = Blueprint("shifts", __name__, url_prefix="/shifts")


@shift_bp.route("", methods=["POST"])
def create_shift():
    data = request.get_json()
    if not data:
        abort(400, description="No input data provided")

    required_fields = ["date", "start_time", "end_time", "technician_id"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing required field: {field}")

    date_obj = parse_date_string(data["date"], "date")
    start_time_obj = parse_time_string(data["start_time"], "start_time")
    end_time_obj = parse_time_string(data["end_time"], "end_time")

    # Validate technician exists
    technician = Technician.query.get(data["technician_id"])
    if not technician:
        abort(404, description=f"Technician with id {data['technician_id']} not found.")

    # Validate equipment exists if provided
    assigned_equipment_id = data.get("assigned_equipment_id")
    if assigned_equipment_id:
        equipment = Equipment.query.get(assigned_equipment_id)
        if not equipment:
            abort(
                404, description=f"Equipment with id {assigned_equipment_id} not found."
            )

    new_shift = Shift(
        date=date_obj,
        start_time=start_time_obj,
        end_time=end_time_obj,
        notes=data.get("notes"),
        technician_id=data["technician_id"],
        assigned_equipment_id=assigned_equipment_id,
    )

    db.session.add(new_shift)
    db.session.commit()

    return (
        jsonify({"message": "Shift created successfully", "shift_id": new_shift.id}),
        201,
    )


@shift_bp.route("", methods=["GET"])
def get_all_shifts():
    shifts = Shift.query.all()
    shifts_data = []
    for shift in shifts:
        shifts_data.append(
            {
                "id": shift.id,
                "date": format_date_field(shift.date),
                "start_time": format_time_field(shift.start_time, "start_time"),
                "end_time": format_time_field(shift.end_time, "end_time"),
                "notes": shift.notes,
                "technician_id": shift.technician_id,
                "assigned_equipment_id": shift.assigned_equipment_id,
            }
        )
    return jsonify(shifts_data), 200


@shift_bp.route("/<int:shift_id>", methods=["GET"])
def get_shift_by_id(shift_id):
    shift = Shift.query.get_or_404(
        shift_id, description=f"Shift with id {shift_id} not found."
    )

    shift_data = {
        "id": shift.id,
        "date": format_date_field(shift.date),
        "start_time": format_time_field(shift.start_time, "start_time"),
        "end_time": format_time_field(shift.end_time, "end_time"),
        "notes": shift.notes,
        "technician_id": shift.technician_id,
        "assigned_equipment_id": shift.assigned_equipment_id,
    }
    return jsonify(shift_data), 200


@shift_bp.route("/<int:shift_id>", methods=["PUT"])
def update_shift(shift_id):
    shift = Shift.query.get_or_404(
        shift_id, description=f"Shift with id {shift_id} not found."
    )
    data = request.get_json()
    if not data:
        abort(400, description="No input data provided for update")

    if "date" in data:
        shift.date = parse_date_string(data["date"], "date")
    if "start_time" in data:
        shift.start_time = parse_time_string(data["start_time"], "start_time")
    if "end_time" in data:
        shift.end_time = parse_time_string(data["end_time"], "end_time")
    if "notes" in data:
        shift.notes = data["notes"]
    if "technician_id" in data:
        technician = Technician.query.get(data["technician_id"])
        if not technician:
            abort(
                404,
                description=f"Technician with id {data['technician_id']} not found.",
            )
        shift.technician_id = data["technician_id"]
    if "assigned_equipment_id" in data:
        assigned_equipment_id = data["assigned_equipment_id"]
        if assigned_equipment_id is not None:  # Allow unassigning by passing null/None
            equipment = Equipment.query.get(assigned_equipment_id)
            if not equipment:
                abort(
                    404,
                    description=f"Equipment with id {assigned_equipment_id} not found.",
                )
        shift.assigned_equipment_id = assigned_equipment_id

    db.session.commit()
    return jsonify({"message": "Shift updated successfully"}), 200


@shift_bp.route("/<int:shift_id>", methods=["DELETE"])
def delete_shift(shift_id):
    shift = Shift.query.get_or_404(
        shift_id, description=f"Shift with id {shift_id} not found."
    )
    db.session.delete(shift)
    db.session.commit()
    return jsonify({"message": "Shift deleted successfully"}), 200
