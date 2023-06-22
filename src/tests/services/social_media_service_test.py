from unittest.mock import AsyncMock

import pytest

from src.adapters.twitter_client import TwitterClient
from src.services.social_media_service import TwitterService


@pytest.fixture
def mock_twitter_client():
    return AsyncMock(spec=TwitterClient)


@pytest.mark.asyncio
async def test_twitter_service_publish(mock_twitter_client):
    # Arrange
    message = "Test message"
    twitter_service = TwitterService(twitter_client=mock_twitter_client)
    mock_twitter_client.publish.return_value = True

    # Act
    result = await twitter_service.publish(message)

    # Assert
    assert result is True
    mock_twitter_client.publish.assert_awaited_once_with(message)


@pytest.mark.asyncio
async def test_twitter_service_publish_failure(mock_twitter_client):
    # Arrange
    message = "Test message"
    twitter_service = TwitterService(twitter_client=mock_twitter_client)
    mock_twitter_client.publish.return_value = False

    # Act
    result = await twitter_service.publish(message)

    # Assert
    assert result is False
    mock_twitter_client.publish.assert_awaited_once_with(message)
