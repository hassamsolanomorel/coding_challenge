"""
Package: app.datasources
Filename: __init__.py
Author(s): Hassam S

Definitions below are mostly expose package modules in a more convenient
way
"""
# Python Imports

# 3rd-Party Imports

# Project Imports
from app.datasources.github import GitHubProfile
from app.datasources.bitbucket import BitBucketProfile
from app.datasources.base import profile_keys

# The keys of this dict ultimately define which values are valid 'sources'
# that the client can specify
class_map = {
    'github': GitHubProfile,
    'bitbucket': BitBucketProfile
}


# Convienence function for getting all valid 'sources'
def all_sources():
    return [key for key in class_map.keys()]
