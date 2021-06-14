"""
Package: app.tests.contracttests
Filename: base.py
Author(s): Hassam S

Base test class for contract tests (integration)
"""
from flask import Flask
from app.routes import configure_routes
import unittest

# The folder where we want to save our VCR recordings
# More on vcrpy : https://vcrpy.readthedocs.io/en/latest/index.html
base_cassette_path = "app/tests/contracttests/recordings/"


class BaseContractTest(unittest.TestCase):
    access_token_str = "access_token=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"

    def setUp(self):
        app = Flask(__name__)
        configure_routes(app)
        self.client = app.test_client()
