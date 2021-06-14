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
    # The following token has been invalidated and will NOT work under
    # regular curcumstances. It is provided here only as a sample of what the
    # 'access_token' query param should look like.
    # NOTE: If tests need to be re-recorded this value must be changed or the
    # tests will NOT pass.
    # TODO: Integrate production ready secret keeping such has Vault so secrets
    # are passed in at runtime
    access_token_str = "access_token=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"

    def setUp(self):
        app = Flask(__name__)
        configure_routes(app)
        self.client = app.test_client()
