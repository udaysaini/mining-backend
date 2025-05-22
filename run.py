import os
from app import create_app
from db_init import init_db

app = create_app()


# Check if we need to initialize the database
def should_init_db():
    # Get database URI from app config
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")

    # For SQLite database
    if db_uri.startswith("sqlite:///"):
        db_path = db_uri.replace("sqlite:///", "")
        # Check if the file exists and has tables
        if not os.path.exists(db_path) or os.path.getsize(db_path) < 100:
            return True

    # Always initialize in Railway environment
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        return True

    return False


if __name__ == "__main__":
    # Initialize database if needed
    if should_init_db():
        print("Database not found or empty. Initializing...")
        # Set this to False in production if you don't want mock data
        init_db(with_mock_data=True)

    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # In production, bind to 0.0.0.0 to accept connections from any source
    app.run(host="0.0.0.0", port=port, debug=False)
