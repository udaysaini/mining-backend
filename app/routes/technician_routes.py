from flask import Blueprint, jsonify, request, abort;
from app import db;
from app.models.technician import Technician;
from datetime import datetime, time;

# Create a blueprint for the technician routes
technician_bp = Blueprint("technicians", __name__, url_prefix="/technicians")

# Route to get all technicians
@technician_bp.route("", methods=["POST"])
def create_technician():
    data = request.get_json()

    #Validate required fields
    if not data or "name" not in data:
        abort(400, "Missing required fields: name")

    print('Data received:', data);

    # Function to parse time strings and prevent SQLite errors
    def parse_time(key):
        time_str = data.get(key)
        if not time_str:
            return None
        # Expecting "HH:MM:SS"; adjust format if you send "HH:MM"
        try:
            parsed_time =  datetime.strptime(time_str, "%H:%M:%S").time()
            print(parsed_time)
            return parsed_time
        except ValueError:
            abort(400, description=f"Invalid time format for {key}. Use HH:MM:SS")

    available_from = parse_time("available_from")
    available_to = parse_time("available_to")

    # Create a new technician instance
    new_technician = Technician(
        name= data["name"],
        role= data.get("role"),
        skills= data.get("skills"),
        available_from= available_from,
        available_to= available_to
    )

    # Add the new technician to the session and commit
    db.session.add(new_technician)
    db.session.commit()

    # Return a success message with the technician ID
    return jsonify({
        "message": "Technician created successfully", 
        "technician_id": new_technician.id
    }), 201

@technician_bp.route("", methods=["GET"])
def get_technicians():
    # Get all technicians from the database
    technicians = Technician.query.all()

    # Convert the list of technicians to a list of dictionaries
    technicians_list = []
    for technician in technicians:
        try: 
            formatted_available_from = technician.available_from.strftime("%H:%M:%S") if technician.available_from else None
            formatted_available_to = technician.available_to.strftime("%H:%M:%S") if technician.available_to else None
        except AttributeError:
            print("Error formatting time for technician:", technician.name)
            formatted_available_from = None
            formatted_available_to = None

        technicians_list.append({
            "id": technician.id,
            "name": technician.name,
            "role": technician.role,
            "skills": technician.skills,
            "available_from": formatted_available_from,
            "available_to": formatted_available_to
        })

    # Return the list of technicians as JSON
    return jsonify(technicians_list), 200

@technician_bp.route("/<int:technician_id>", methods=["GET"])
def get_technician(technician_id):
    # get a specific technician by ID
    technician = Technician.query.get_or_404(
        technician_id, 
        description=f"No technician found with id={technician_id}"
    )

    # technician = Technician.query.get(technician_id)
    # if not technician:
    #     abort(404, description=f"No technician found with id={technician_id}")

    try:
        formatted_available_from = technician.available_from.strftime("%H:%M:%S") if technician.available_from else None
        formatted_available_to = technician.available_to.strftime("%H:%M:%S") if technician.available_to else None  
    except AttributeError:
        print("Error formatting time for technician:", technician.name)
        formatted_available_from = None
        formatted_available_to = None
    
    # Convert the technician object to a dictionary
    technician_data = {
        "id": technician.id,
        "name": technician.name,
        "role": technician.role,
        "skills": technician.skills,
        "available_from": formatted_available_from,
        "available_to": formatted_available_to
    }

    return jsonify(technician_data), 200