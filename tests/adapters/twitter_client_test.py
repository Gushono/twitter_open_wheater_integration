from unittest.mock import Mock

import pytest
import tweepy

from src.adapters.twitter_client import TwitterClient
from src.exceptions.client_exceptions import TwitterSendMessageException


@pytest.fixture
def mock_tweepy_client(monkeypatch):
    mock_client = Mock(spec=tweepy.Client)
    monkeypatch.setattr(tweepy, 'Client', mock_client)
    return mock_client


@pytest.fixture
def mock_env_variables_twitter(monkeypatch):
    monkeypatch.setenv("TWITTER_BEARER_TOKEN", "bearer_token")
    monkeypatch.setenv("TWITTER_CONSUMER_KEY", "consumer_key")
    monkeypatch.setenv("TWITTER_CONSUMER_SECRET", "consumer_secret")
    monkeypatch.setenv("TWITTER_ACCESS_TOKEN", "access_token")
    monkeypatch.setenv("TWITTER_ACCESS_TOKEN_SECRET", "access_token_secret")


def test_twitter_client_init_with_credentials_from_env(mock_tweepy_client, mock_env_variables_twitter):
    twitter_client = TwitterClient()

    assert twitter_client._bearer_token == "bearer_token"
    assert twitter_client._consumer_key == "consumer_key"
    assert twitter_client._consumer_secret == "consumer_secret"
    assert twitter_client._access_token == "access_token"
    assert twitter_client._access_token_secret == "access_token_secret"
    mock_tweepy_client.assert_called_once_with(
        "bearer_token",
        "consumer_key",
        "consumer_secret",
        "access_token",
        "access_token_secret"
    )
    assert twitter_client.client == mock_tweepy_client.return_value
    mock_tweepy_client.return_value.create_tweet.assert_not_called()


@pytest.mark.asyncio
async def test_twitter_client_publish_success(mock_tweepy_client, mock_env_variables_twitter):
    twitter_client = TwitterClient()
    mock_tweepy_client.return_value.create_tweet.return_value = True

    result = await twitter_client.publish("Hello, world!")

    assert result is True
    mock_tweepy_client.return_value.create_tweet.assert_called_once_with(text="Hello, world!")
    mock_tweepy_client.return_value.create_tweet.reset_mock()


@pytest.mark.asyncio
async def test_twitter_client_publish_failure(mock_tweepy_client, mock_env_variables_twitter):
    twitter_client = TwitterClient()
    mock_tweepy_client.return_value.create_tweet.return_value = False

    with pytest.raises(TwitterSendMessageException):
        await twitter_client.publish("Hello, world!")

    mock_tweepy_client.return_value.create_tweet.assert_called_once_with(text="Hello, world!")
    mock_tweepy_client.return_value.create_tweet.reset_mock()
