from datetime import datetime, time
from flask import current_app
from flask import abort


def format_time(time_obj):
    """
    Format a time object to a string in HH:MM:SS format.
    """
    if isinstance(time_obj, time):
        return time_obj.strftime("%H:%M:%S")
    elif isinstance(time_obj, str):
        try:
            # Attempt to parse the string as a time
            parsed_time = datetime.strptime(time_obj, "%H:%M:%S").time()
            return parsed_time.strftime("%H:%M:%S")
        except ValueError:
            current_app.logger.error(f"Invalid time format: {time_obj}")
            return None
    else:
        current_app.logger.error(
            f"Unsupported type for time formatting: {type(time_obj)}"
        )
        return None


def parse_time_string(time_str, field_name=None):
    """
    Parse a time string into a time object.

    Args:
        time_str: String representation of time (e.g., "14:30:00" or "14:30")
        field_name: Optional name of the field for error messages

    Returns:
        datetime.time object or None if time_str is None
    """
    if not time_str:
        return None

    # Try different time formats
    formats = ["%H:%M:%S", "%H:%M"]

    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue

    # If we get here, none of the formats worked
    error_msg = "Invalid time format"
    if field_name:
        error_msg += f" for {field_name}"
    error_msg += ". Use HH:MM:SS or HH:MM"

    abort(400, description=error_msg)


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
            "Failed to format field '%s': %r — %s", field_name, t, e
        )
        return None
