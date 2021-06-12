from abc import ABC
from abc import abstractmethod
from collections import defaultdict


class BaseDataSource(ABC):

    user_profile = defaultdict(lambda: None)

    profile_keys = [
        'num_original_repos',
        'num_forked_repos',
        'total_repos',
        'num_watchers',
        'language_stats',
        'topic_stats'
    ]

    def __init__(self, user_name: str, access_token: str = None):
        self.user_name = user_name

    @abstractmethod
    def get_profile_summary(self):
        pass
