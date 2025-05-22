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


def parse_date_string(date_str, field_name=None):
    """
    Parse a date string into a date object.

    Args:
        date_str: String representation of date (e.g., "YYYY-MM-DD")
        field_name: Optional name of the field for error messages

    Returns:
        datetime.date object or None if date_str is None
    """
    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        error_msg = "Invalid date format"
        if field_name:
            error_msg += f" for {field_name}"
        error_msg += ". Use YYYY-MM-DD"
        abort(400, description=error_msg)


def format_date_field(date_obj):
    """
    Format a date object to a string in YYYY-MM-DD format.
    """
    if date_obj is None:
        return None
    if isinstance(date_obj, str):
        try:
            # Validate if the string is already in the correct format or parseable
            parsed_date = datetime.strptime(date_obj, "%Y-%m-%d").date()
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            current_app.logger.error(f"Invalid date string for formatting: {date_obj}")
            return None  # Or raise an error, or return original string
    elif isinstance(
        date_obj, datetime
    ):  # Handle datetime objects by converting to date
        return date_obj.date().strftime("%Y-%m-%d")
    elif hasattr(date_obj, "strftime"):  # Handles date objects
        return date_obj.strftime("%Y-%m-%d")
    else:
        current_app.logger.error(
            f"Unsupported type for date formatting: {type(date_obj)}"
        )
        return None
