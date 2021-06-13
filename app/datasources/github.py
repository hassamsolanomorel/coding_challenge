"""
Package: app.datasources
Filename: github.py
Author(s): Hassam S

Define interactions with the Github datasource
"""
# Python Imports
from collections import defaultdict

# 3rd-Party Imports
from github import Github

# Project Imports
from app.datasources.base import BaseDataSource


class GitHubProfile(BaseDataSource):
    """
    This class defines the functions required to get a summary profile for a
    given user/organization/team from the GitHub API

    Author's Note: Here we show and example of interacting with an API, for
        which a Python library is available.

    Relevant Docs:
        - GitHub API: https://docs.github.com/en/rest
        - PyGithub: https://pygithub.readthedocs.io/en/latest/index.html
    """

    _client = Github()

    def __init__(self, user_name: str, **kwargs):
        super().__init__(user_name, **kwargs)
        if self.access_token:
            self._client = Github(self.access_token)

    def _build_profile_summary(self):
        # Total number of public repos (original repos vs forked repos)
        num_org_repos = 0
        num_forked_repos = 0
        # Total watcher/follower count for repos
        repo_followers = 0
        # A list/count of languages used across all public repos
        lang_stats = defaultdict(lambda: 0)
        # A list/count of repo topics
        topics = defaultdict(lambda: 0)

        for repo in self._client.get_user(self.user_name).get_repos():
            # Get repo count (Original vs Forked)
            if repo.fork:
                num_forked_repos += 1
            else:
                num_org_repos += 1

            # Get total repo watchers/followers
            # NOTE: After reading through the GitHub API changes it looks like
            # subscribers_count is the number of people "watching" the repo
            # while watchers_count/watchers is the number of people who have
            # starred the repo. Based on challenge description we summate
            # subscribers_count values below.
            repo_followers += repo.subscribers_count

            # Get repo languages
            # TODO: Optimize using AsyncIO
            #   We could be making these requests concurrently which would
            #   DRAMATICALLY improve performance here. Flask + AsyncIO requires
            #   Python 3.7+
            for key in repo.get_languages().keys():
                lang_stats[key.capitalize()] += 1

            # Get repo topics
            # TODO: Optimize using AsyncIO
            for topic in repo.get_topics():
                topics[topic] += 1

        user_profile = {
            'num_original_repos': num_org_repos,
            'num_forked_repos': num_forked_repos,
            'total_repos': num_org_repos + num_forked_repos,
            'num_watchers': repo_followers,
            'language_stats': dict(lang_stats),
            'topic_stats': dict(topics)
        }
        return user_profile
