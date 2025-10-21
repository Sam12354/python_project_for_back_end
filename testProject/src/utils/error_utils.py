def get_error_message(err):
    """
    Extracts a friendly error message from an exception.

    - If it's a ValidationError (like from SQLAlchemy or your custom error),
      it grabs the first error message from the error details.
    - Otherwise, it returns the general error message.
    """
    # Check if error has a 'name' attribute and if it's 'ValidationError'
    if getattr(err, 'name', None) == 'ValidationError':
        # getattr(object, 'attribute', default) tries to get 'attribute' from 'object';
        # Try to get the first error message from err.errors dictionary
        errors = getattr(err, 'errors', {})
        if errors:
            # return first error message
            first_error = next(iter(errors.values()))
            return getattr(first_error, 'message', str(first_error))
        else:
            return str(err)
    else:
        # Default: just return the error message
        return str(err)
