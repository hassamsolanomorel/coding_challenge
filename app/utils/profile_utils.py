"""
Package: app.utils
Filename: profile_utils.py
Author(s): Hassam S

Define utility functions related to working with already completed profiles
"""
# Python Imports
from collections import defaultdict

# 3rd-Party Imports

# Project Imports

_DEFAULT_DICT_VALUE = 0


def merge_profiles(profiles: [dict], keys: [str]):
    # This function is written as a utility to combine multiple datasource
    # profiles together. The logic makes assumptions on value types based on
    # the criteria given in the coding assignment instructions. A more generic
    # solution would likely be more complex and not needed at this time.

    unified_profile = defaultdict(lambda: _DEFAULT_DICT_VALUE)

    for profile in profiles:
        for key in keys:
            # Account for missing values in the profile
            if not profile.get(key):
                continue

            # The following logic ASSUMES that profile values will be either
            # dicts or an int. A more generic strategy could likely be applied
            # here.
            if type(profile[key]) is dict:
                # We need to combine 2 dicts here
                # First check if current value is a dict
                if type(unified_profile[key]) is not dict:
                    unified_profile[key] = dict()
                # Now that we KNOW there is a dict we can combine
                unified_profile[key] = _combine_dicts([unified_profile[key],
                                                      profile[key]])

            else:  # Value is an int (ASSUMPTION)
                unified_profile[key] += profile[key]

    return unified_profile


def _combine_dicts(dicts: [dict]):
    # This logic ASSUMES dict values are ints
    unified_dict = defaultdict(lambda: _DEFAULT_DICT_VALUE)
    for d in dicts:
        for k, v in d.items():
            if d[k]:
                unified_dict[k] += v

    return dict(unified_dict)
