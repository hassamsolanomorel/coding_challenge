import flask
from flask import Flask
import logging
from app.routes import configure_routes


app = Flask("user_profiles_api")

configure_routes(app)

logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)
