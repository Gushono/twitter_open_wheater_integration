from abc import ABC

from src.adapters.twitter_client import TwitterClient, TweepyClient


class SocialMediaService(ABC):

    async def publish(self, message: str) -> bool:  # pragma: no cover
        raise NotImplementedError


class TwitterService(SocialMediaService):
    def __init__(self, twitter_client: TwitterClient = None):
        self.twitter_client = twitter_client if twitter_client else TweepyClient()

    async def publish(self, message: str) -> bool:
        return await self.twitter_client.publish(message)
