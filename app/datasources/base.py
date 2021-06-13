"""
Package: app.datasources
Filename: base.py
Author(s): Hassam S

Define datasource class interface and define some common functions
"""
# Python Imports
from abc import ABC
from abc import abstractmethod

# 3rd-Party Imports

# Project Imports

# In case a value is missing from a profile summary we use this value
_DEFAULT_VALUE = None

# The expected keys for profile summaries
profile_keys = [
    'num_original_repos',
    'num_forked_repos',
    'total_repos',
    'num_watchers',
    'language_stats',
    'topic_stats'
]


class BaseDataSource(ABC):
    """
    Define the abstract interface for all datasources
    """

    def __init__(self, user_name: str, **kwargs):
        self.user_name = user_name

        if kwargs:
            self.access_token = kwargs.get('access_token')

    @abstractmethod
    def _build_profile_summary(self):
        # This will be slightly different for every datasource, so it must be
        # abstract.
        pass

    def get_profile_summary(self):
        # This function ensures that ALL expected profile keys will exist.
        # Values are defaulted to a specified value IFF the key does NOT
        # already exist in the profile
        profile = self._build_profile_summary()
        for key in profile_keys:
            if key not in profile:
                profile[key] = _DEFAULT_VALUE

        return profile
