from github import Github
from collections import defaultdict
from app.datasources.base import BaseDataSource


class GitHubProfile(BaseDataSource):

    _client = Github("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")

    def get_profile_summary(self):
        # Total number of public repos (original repos vs forked repos)
        num_org_repos = 0
        num_forked_repos = 0
        # ○ Total watcher/follower count for repos
        repo_followers = 0
        # ○ A list/count of languages used across all public repos
        # ○ A list/count of repo topics
        topics = defaultdict(lambda: 0)
        lang_stats = defaultdict(lambda: 0)

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

            # Get repo topics
            # TODO: Optimize using AsyncIO
            for topic in repo.get_topics():
                topics[topic] += 1

            # Get repo languages
            # TODO: Optimize using AsyncIO
            for key in repo.get_languages().keys():
                lang_stats[key.capitalize()] += 1

        self.user_profile = {
            'num_original_repos': num_org_repos,
            'num_forked_repos': num_forked_repos,
            'total_repos': num_org_repos + num_forked_repos,
            'num_watchers': repo_followers,
            'language_stats': dict(lang_stats),
            'topic_stats': dict(topics)
        }
        return self.user_profile
