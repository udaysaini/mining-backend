import sys
import os
from datetime import datetime, timedelta, time
import random

# Add the parent directory to the path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db, create_app
from app.models.equipment import Equipment
from app.models.technician import Technician
from app.models.shift import Shift

app = create_app()


def reset_database():
    """Drop all tables and recreate them"""
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()


def populate_technicians():
    """Add mock technicians to the database"""
    with app.app_context():
        print("Adding technicians...")

        # Updated technician data to match the actual model
        roles = [
            "Senior Technician",
            "Junior Technician",
            "Lead Engineer",
            "Maintenance Specialist",
            "Safety Officer",
        ]
        skills_list = [
            "Electrical Troubleshooting, Wiring, Circuit Design",
            "Mechanical Repair, Hydraulic Systems, Welding",
            "Automation, PLC Programming, Sensors",
            "Heavy Equipment Operation, Machinery Maintenance",
            "Safety Protocols, Emergency Response, First Aid",
            "Electronics, Microcontrollers, Diagnostics",
            "Pneumatic Systems, Pressure Testing, Valve Repair",
            "Structural Analysis, Metal Fabrication",
            "Computer Systems, SCADA, Network Infrastructure",
            "Quality Control, Inspection, Documentation",
        ]

        # Create shift timings for technicians
        morning_shift = {"available_from": time(6, 0), "available_to": time(14, 0)}
        afternoon_shift = {"available_from": time(14, 0), "available_to": time(22, 0)}
        night_shift = {"available_from": time(22, 0), "available_to": time(6, 0)}
        shifts = [morning_shift, afternoon_shift, night_shift]

        tech_data = [
            {
                "name": "John Smith",
                "role": random.choice(roles),
                "skills": skills_list[0],
                **random.choice(shifts),
            },
            {
                "name": "Maria Rodriguez",
                "role": random.choice(roles),
                "skills": skills_list[1],
                **random.choice(shifts),
            },
            {
                "name": "David Chen",
                "role": random.choice(roles),
                "skills": skills_list[2],
                **random.choice(shifts),
            },
            {
                "name": "Sarah Johnson",
                "role": random.choice(roles),
                "skills": skills_list[3],
                **random.choice(shifts),
            },
            {
                "name": "Michael Brown",
                "role": random.choice(roles),
                "skills": skills_list[4],
                **random.choice(shifts),
            },
            {
                "name": "Emily Davis",
                "role": random.choice(roles),
                "skills": skills_list[5],
                **random.choice(shifts),
            },
            {
                "name": "Robert Wilson",
                "role": random.choice(roles),
                "skills": skills_list[6],
                **random.choice(shifts),
            },
            {
                "name": "Jennifer Lee",
                "role": random.choice(roles),
                "skills": skills_list[7],
                **random.choice(shifts),
            },
            {
                "name": "William Garcia",
                "role": random.choice(roles),
                "skills": skills_list[8],
                **random.choice(shifts),
            },
            {
                "name": "Laura Martinez",
                "role": random.choice(roles),
                "skills": skills_list[9],
                **random.choice(shifts),
            },
        ]

        for tech in tech_data:
            technician = Technician(**tech)
            db.session.add(technician)

        db.session.commit()
        print(f"Added {len(tech_data)} technicians")


def populate_equipment():
    """Add mock equipment to the database"""
    with app.app_context():
        print("Adding equipment...")

        # Get all technician IDs for random assignment
        technicians = Technician.query.all()
        tech_ids = [tech.id for tech in technicians]

        equipment_types = [
            "Excavator",
            "Loader",
            "Bulldozer",
            "Drill",
            "Crusher",
            "Conveyor",
            "Truck",
            "Pump",
            "Generator",
        ]
        locations = [
            "Mine Shaft A",
            "Mine Shaft B",
            "Processing Plant",
            "Storage Yard",
            "Main Site",
            "Quarry",
            "Refinery",
        ]
        statuses = ["operational", "maintenance", "repair", "standby", "decommissioned"]

        today = datetime.now().date()

        # Updated equipment data to match the actual model
        equipment_data = [
            {
                "name": f"{random.choice(['Heavy', 'Light', 'Medium', 'Industrial', 'Compact'])} {eq_type} {i+1}",
                "type": eq_type,
                "location": random.choice(locations),
                "status": random.choice(statuses),
                "last_maintenance": (today - timedelta(days=random.randint(0, 365))),
                "assigned_to": (
                    random.choice(tech_ids) if random.random() > 0.3 else None
                ),  # 70% chance of being assigned
            }
            for i, eq_type in enumerate(random.choices(equipment_types, k=10))
        ]

        for equip in equipment_data:
            equipment = Equipment(**equip)
            db.session.add(equipment)

        db.session.commit()
        print(f"Added {len(equipment_data)} equipment items")


def populate_shifts():
    """Add mock shifts to the database"""
    with app.app_context():
        print("Adding shifts...")

        # Get all technicians and equipment for assignment
        technicians = Technician.query.all()
        equipment = Equipment.query.all()

        # Define shift times
        shift_times = [
            {"start": time(6, 0), "end": time(14, 0)},  # Morning shift: 6 AM - 2 PM
            {"start": time(14, 0), "end": time(22, 0)},  # Afternoon shift: 2 PM - 10 PM
            {"start": time(22, 0), "end": time(6, 0)},  # Night shift: 10 PM - 6 AM
        ]

        # Create dates for the last 7 days plus 3 days in the future
        today = datetime.now().date()
        dates = [(today - timedelta(days=i)) for i in range(7)]
        dates.extend([(today + timedelta(days=i)) for i in range(1, 4)])

        shift_data = []

        # Create 10 random shifts
        for i in range(10):
            # Select a random technician and date
            technician = random.choice(technicians)
            date = random.choice(dates)

            # Match the shift time to the technician's availability when possible
            if technician.available_from and technician.available_to:
                start_time = technician.available_from
                end_time = technician.available_to
            else:
                shift_time = random.choice(shift_times)
                start_time = shift_time["start"]
                end_time = shift_time["end"]

            # 80% chance of having equipment assigned
            assigned_equipment = (
                random.choice(equipment) if random.random() < 0.8 else None
            )
            equipment_id = assigned_equipment.id if assigned_equipment else None

            # Generate random notes
            note_options = [
                "Regular maintenance work",
                "Equipment inspection",
                "Emergency repair",
                "Safety training session",
                "Scheduled maintenance",
                "System upgrade",
                "Troubleshooting",
                "Performance testing",
                "Cleaning and servicing",
                "Parts replacement",
            ]

            shift = {
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "technician_id": technician.id,
                "assigned_equipment_id": equipment_id,
                "notes": (
                    random.choice(note_options) if random.random() < 0.7 else None
                ),  # 70% chance of having notes
            }

            shift_data.append(shift)

        for shift in shift_data:
            new_shift = Shift(**shift)
            db.session.add(new_shift)

        db.session.commit()
        print(f"Added {len(shift_data)} shifts")


def main():
    """Main function to reset and populate the database"""
    print("Starting database reset and population...")
    reset_database()
    populate_technicians()
    populate_equipment()
    populate_shifts()  # Add shifts after technicians and equipment
    # Add other populate functions for additional models
    print("Database reset and population complete!")


if __name__ == "__main__":
    main()
