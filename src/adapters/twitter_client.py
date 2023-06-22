import os
import tweepy

from src.exceptions.client_exceptions import TwitterSendMessageException


class TwitterClient:
    def __init__(
        self,
        bearer_token: str = None,
        consumer_key: str = None,
        consumer_secret: str = None,
        access_token: str = None,
        access_token_secret: str = None,
    ):
        self._bearer_token = bearer_token or os.getenv("TWITTER_BEARER_TOKEN")
        self._consumer_key = consumer_key or os.getenv("TWITTER_CONSUMER_KEY")
        self._consumer_secret = consumer_secret or os.getenv("TWITTER_CONSUMER_SECRET")
        self._access_token = access_token or os.getenv("TWITTER_ACCESS_TOKEN")
        self._access_token_secret = access_token_secret or os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        self.client = tweepy.Client(
            self._bearer_token,
            self._consumer_key,
            self._consumer_secret,
            self._access_token,
            self._access_token_secret,
        )
        self.authenticate()

    def authenticate(self):
        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)
        return tweepy.API(auth)

    async def publish(self, message: str):
        success = self.client.create_tweet(text=message)
        if not success:
            raise TwitterSendMessageException()
        print(success)
        return success
