from enum import Enum
from typing import List, Optional

class Trend:
    url: str
    name: str
    query: str
    tweet_volume: Optional[int]
    promoted_content: None

    def __init__(self, url: str, name: str, query: str, tweet_volume: Optional[int], promoted_content: None) -> None:
        self.url = url
        self.name = name
        self.query = query
        self.tweet_volume = tweet_volume
        self.promoted_content = promoted_content
