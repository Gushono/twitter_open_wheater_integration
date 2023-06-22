from abc import ABC

from src.adapters.twitter_client import TwitterClient


class SocialMediaService(ABC):

    async def publish(self, message: str) -> bool:
        raise NotImplementedError


class TwitterService(SocialMediaService):
    def __init__(self, twitter_client: TwitterClient = None):
        self.twitter_client = twitter_client if twitter_client else TwitterClient()

    async def publish(self, message: str) -> bool:
        return await self.twitter_client.publish(message)
