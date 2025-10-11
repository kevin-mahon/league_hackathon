import re

class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

def validate_field(
        #update field type to allow array of types [str, int, float]
    value,
    field_type=str,
    *,
    required=True,
    min_length=None,
    max_length=None,
    regex=None,
    choices=None
):
    """
    Validates a single field with customizable rules.
    Raises ValidationError if invalid, returns cleaned value if valid.
    """

    # Handle required / null
    if value is None or (isinstance(value, str) and value.strip() == ""):
        if required:
            raise ValidationError("This field is required.")
        return None

    # Type check
    if not isinstance(value, field_type):
        raise ValidationError(f"Expected {field_type.__name__}, got {type(value).__name__}")

    # String length checks
    if isinstance(value, str):
        if min_length is not None and len(value) < min_length:
            raise ValidationError(f"Must be at least {min_length} characters long.")
        if max_length is not None and len(value) > max_length:
            raise ValidationError(f"Must be at most {max_length} characters long.")

    # Regex check
    if regex and not re.match(regex, str(value)):
        raise ValidationError("Invalid format.")

    # Choices check
    if choices and value not in choices:
        raise ValidationError(f"Value must be one of: {choices}")

    return value
