import os

import tweepy

from src.exceptions.client_exceptions import TwitterSendMessageException

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


class TwitterClient:

    def __init__(self):
        self.client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
        self.authenticate()

    @staticmethod
    def authenticate():
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    async def publish(self, message: str):
        # success = self.client.create_tweet(text=message)
        print(message)
        success = True
        if not success:
            raise TwitterSendMessageException()
        print(success)
        return success
