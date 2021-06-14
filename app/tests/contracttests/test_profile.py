"""
Package: app.tests.contracttests
Filename: test_profile.py
Author(s): Hassam S

Tests for the profiles endpoint
"""
# Python Imports
import json

# 3rd-Party Imports
import vcr  # We use this so we don't require a network connection to test

# Project Imports
from app.tests.contracttests.base import BaseContractTest
from app.tests.contracttests.base import base_cassette_path
from app.datasources.base import profile_keys


# Known Issues:
#   1) Hitting the endpoint with a user that does not exist at a datasource
#       can cause the whole request to fail. This doesn't sound right.
class TestProfile(BaseContractTest):
    base_url = '/profile/mailchimp'
    cassette_path = base_cassette_path + 'TestProfile_test_get_profile_200.yml'

    @vcr.use_cassette(cassette_path)
    def test_get_profile_200(self):
        url = f'/profile/mailchimp?{self.access_token_str}'
        response = self.client.get(url)

        data = json.loads(response.get_data())

        assert response.status_code == 200

        for key in profile_keys:
            assert key in data

    def test_get_profile_missing_token_400(self):
        url = '/profile/mailchimp'
        response = self.client.get(url)
        assert response.status_code == 400

    def test_get_profile_invalid_token_500(self):
        url = self.base_url + '?access_token=1234FAKE'
        response = self.client.get(url)
        assert response.status_code == 500

    @vcr.use_cassette(cassette_path)
    def test_get_profile_valid_sources_200(self):
        url = f'/profile/mailchimp?{self.access_token_str}&sources=bitbucket'
        response = self.client.get(url)

        data = json.loads(response.get_data())
        assert 'num_watchers' in data
        assert response.status_code == 200

    def test_get_profile_invaid_source_400(self):
        url = self.base_url + f'?{self.access_token_str}&sources=INVALID'
        response = self.client.get(url)
        assert response.status_code == 400
