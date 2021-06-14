from app.application import app


if __name__ == '__main__':
    # Using host 0.0.0.0 makes dockerizing the app just a bit easier
    app.run(debug=True, host='0.0.0.0')
