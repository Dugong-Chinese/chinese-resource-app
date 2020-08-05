"""Entry point for the API."""

from init import create_app


if __name__ == "__main__":
    # Locally, create a sibling file to api.py, "local_settings.py"
    # and put `debug = True` in it to run the API in debug mode.
    # In production, this will automatically default to False.
    try:
        import local_settings

        debug = local_settings.debug
    except (ImportError, AttributeError):
        debug = False
    debug = bool(debug)
    
    app = create_app()
    app.run(debug=debug)
