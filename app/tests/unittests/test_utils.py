"""
Package: app.tests.unittests
Filename: test_utils.py
Author(s): Hassam S

Tests for util functions
"""
# Python Imports
import unittest

# 3rd-Party Imports

# Project Imports
from app.utils import profile_utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.profile_a = {
            'a': 1,
            'b': None,
            'd': {
                'e': 10
            },
            'f': {
                'g': 5
            }
        }

        self.profile_b = {
            'a': 1,
            'b': 1,
            'd': {
                'e': 10
            },
            'f': {
                'g': None
            }
        }

        self.expected_keys = ['a', 'b', 'd', 'f']

    def test_merge_profiles(self):
        profiles = [self.profile_a, self.profile_b]
        unified_dict = profile_utils.merge_profiles(profiles,
                                                    self.expected_keys)

        for key in self.expected_keys:
            assert key in unified_dict

        assert unified_dict['a'] == 2
        assert unified_dict['b'] == 1
        # The following effectively test _combine_dicts
        assert unified_dict['d']['e'] == 20
        assert unified_dict['f']['g'] == 5
