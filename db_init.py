import os
import sys
from app import create_app, db

# Import the mock data population functions
from scripts.reset_db_with_mock_data import (
    populate_technicians,
    populate_equipment,
    populate_shifts,
)


def init_db(with_mock_data=True):
    """Initialize the database and optionally populate it with mock data"""
    app = create_app()

    with app.app_context():
        print("Creating database tables...")
        db.create_all()

        if with_mock_data:
            print("Populating database with mock data...")
            populate_technicians()
            populate_equipment()
            populate_shifts()

        print("Database initialization complete!")


if __name__ == "__main__":
    # Check if mock data should be included
    mock_data = True
    if len(sys.argv) > 1 and sys.argv[1].lower() == "no-mock":
        mock_data = False

    init_db(with_mock_data=mock_data)
