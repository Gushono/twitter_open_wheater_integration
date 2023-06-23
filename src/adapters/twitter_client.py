import os

import tweepy

from src.exceptions.client_exceptions import TwitterSendMessageException


class TwitterClient:
    def __init__(self, client: tweepy.Client = None):
        self._bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        self._consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
        self._consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
        self._access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self._access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        self.client = client or self.create_client()

    def create_client(self) -> tweepy.Client:
        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)
        return tweepy.Client(
            self._bearer_token,
            self._consumer_key,
            self._consumer_secret,
            self._access_token,
            self._access_token_secret,
        )

    async def publish(self, message: str):
        success = self.client.create_tweet(text=message)
        if not success:
            raise TwitterSendMessageException()
        return success
