from app import create_app, db

# Create app instance using our factory
app = create_app();

# Wrap in app context so Flask can access configuration and models
with app.app_context():
    # Create the database and tables
    db.create_all()
    print("✅ Database and all tables created successfully.")