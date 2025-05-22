import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # In production, bind to 0.0.0.0 to accept connections from any source
    app.run(host="0.0.0.0", port=port, debug=False)
