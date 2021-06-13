"""
Package: app.datasources
Filename: bitbucket.py
Author(s): Hassam S

Define interactions with the Bitbucket datasource
"""
# Python Imports
from collections import defaultdict

# 3rd-Party Imports
import requests

# Project Imports
from app.datasources.base import BaseDataSource


class BitBucketProfile(BaseDataSource):
    """
    This class defines the functions required to get a summary profile for a
    given user/organization/team from the Bitbucket API

    Author's Note: While there is a Python library for the Bitbucket API:
        https://pypi.org/project/atlassian-python-api/
        For this class implemantation I decided use the requests library for
        the following reasons:
        1) In this case the Python library just made things more complicated.
             Because the Bitbucket API is very accomodating for unauthenticated
             clients, it was actually relatively straightforward to just hit
             the needed endpoints directly.
        2) The Python library includes a BUNCH of things that are not currently
            required for this service.
        3) To demonstrate a variety of ways to interact with 3rd-Party APIs.

    Relevant Docs:
        - Bitbucket API: https://developer.atlassian.com/bitbucket/api/2/reference/
    """

    base_repo_url = "https://api.bitbucket.org/2.0/repositories/{org_name}"
    repo_fields = {'fields': "size,values.language,values.links.watchers"}

    def _get_total_watchers(self, url):
        # Since we only care about the NUMBER of watchers, we can omit
        # returning any detailed info
        url += "?fields=size"
        return int(requests.get(url).json().get('size', 0))

    def _build_profile_summary(self):
        # Get repos
        resp = requests.get(
            self.base_repo_url.format(org_name=self.user_name),
            params=self.repo_fields
        ).json()

        # Total number of public repos (original repos vs forked repos)
        # NOTE: As best I was able to investigate, I do NOT believe the
        #   Bitbucket API has a value for differentiating between original and
        #   forked repos. Logic below should be easily extenable if this is
        #   incorrect.
        num_repos = resp.get('size', 0)

        # Process repo info
        repos = resp.get('values', [])
        num_watchers = 0
        lang_stats = defaultdict(lambda: 0)
        # There would be a variable for gathering "topics" here, but I do NOT
        #   believe that is a thing in Bitbucket.
        for repo in repos:
            # Bitbucket reports at MOST one language for a repo
            if repo.get('language'):
                lang_stats[repo.get('language').capitalize()] += 1
            # Since we can't call .get() on None, the logic below looks a bit
            #   redundant, but thats Python! Nested values in http response
            #   objects can get pretty nasty to process.
            if repo.get('links') and repo.get('links').get('watchers'):
                num_watchers += self._get_total_watchers(
                    repo.get('links').get('watchers').get('href')
                )

        user_profile = {
            'total_repos': num_repos,
            'num_watchers': num_watchers,
            'language_stats': dict(lang_stats),
        }

        return user_profile
