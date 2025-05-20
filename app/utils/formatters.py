from datetime import datetime, time
from flask import current_app

def format_time_field(t, field_name):
    """
    Format a time field to a string in HH:MM:SS format.
    """
    # Check if the time is None
    if t is None:
        return None

    # Check if it’s already a time object
    if isinstance(t, time):
        return t.strftime("%H:%M:%S")

    # Check if it’s a string
    try:
        # Try parsing a string like "08:00:00"
        parsed_time = datetime.strptime(t, "%H:%M:%S").time()
        return parsed_time.isoformat()
    except Exception as e:
        current_app.logger.error(
            "Failed to format field '%s': %r — %s",
            field_name, t, e
        )
        return None