"""Entry point for the API."""

from init import create_app


if __name__ == "__main__":
    # Locally, copy `local_settings_example.py`, remove `_example`, and set
    #  debug mode to True.
    # In production, ensure debug mode is disabled.
    try:
        import local_settings

        debug = local_settings.DEBUG
    except (ImportError, AttributeError):
        debug = False
    debug = bool(debug)

    app = create_app()
    app.run(debug=debug)
