import os
from app.application import app


if __name__ == '__main__':
    flask_addr = os.environ.get("FLASK_ADDRESS")
    if flask_addr:
        # Using host 0.0.0.0 makes dockerizing the app just a bit easier
        app.run(debug=True, host=flask_addr)
    else:
        app.run(debug=True)
