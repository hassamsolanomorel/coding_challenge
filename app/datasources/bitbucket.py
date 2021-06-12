import requests
from collections import defaultdict
from app.datasources.base import BaseDataSource


class BitBucketProfile(BaseDataSource):

    base_repo_url = "https://api.bitbucket.org/2.0/repositories/{org_name}"
    repo_fields = {'fields': "size,values.language,values.links.watchers"}

    def _get_total_watchers(self, url):
        # Since we only care about the NUMBER of watchers, we can omit
        # returning any detailed info
        url += "?fields=size"
        return int(requests.get(url).json().get('size', 0))

    def get_profile_summary(self):
        # Get repos
        resp = requests.get(
            self.base_repo_url.format(org_name=self.user_name),
            params=self.repo_fields
        ).json()

        # print(f"\n\n{resp.get('size', 0)}\n\n")

        # Total number of public repos (original repos vs forked repos)
        num_repos = resp.get('size', 0)
        # Process repo info
        repos = resp.get('values', [])

        num_watchers = 0

        lang_stats = defaultdict(lambda: 0)
        for repo in repos:
            if repo.get('language', None):
                lang_stats[repo.get('language').capitalize()] += 1
            if repo.get('links') and repo.get('links').get('watchers'):
                num_watchers += self._get_total_watchers(
                    repo.get('links').get('watchers').get('href')
                )

        print(num_watchers)

        self.user_profile = {
            'num_original_repos': None,
            'num_forked_repos': None,
            'total_repos': num_repos,
            'num_watchers': num_watchers,
            'language_stats': dict(lang_stats),
            'topic_stats': None
        }

        return self.user_profile
