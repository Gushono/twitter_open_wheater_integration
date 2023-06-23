from unittest.mock import AsyncMock

import pytest

from src.adapters.weathermap_client import OpenWeatherMapAPIClient
from src.exceptions.client_exceptions import NotAuthorizedException


@pytest.fixture
def mock_http_client():
    class MockHttpClient:
        pass

    return MockHttpClient()


@pytest.fixture
def client(mock_http_client):
    return OpenWeatherMapAPIClient(http_client=mock_http_client)


class FakeResponse:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data


@pytest.mark.asyncio
async def test_get_weather_for_next_five_days_success(client, mock_http_client):
    mock_http_client.get = AsyncMock(return_value=FakeResponse(200, data={"data": "dummy"}))
    lat = 123.456
    lon = 789.012
    result = await client.get_weather_for_next_five_days(lat, lon)
    assert result == {"data": "dummy"}


@pytest.mark.asyncio
async def test_get_weather_for_next_five_days_not_authorized(client, mock_http_client):
    mock_http_client.get = AsyncMock(return_value=FakeResponse(401, data={}))
    lat = 123.456
    lon = 789.012
    with pytest.raises(NotAuthorizedException):
        await client.get_weather_for_next_five_days(lat, lon)


@pytest.mark.asyncio
async def test_get_weather_for_next_five_days_unknown_code(client, mock_http_client):
    mock_http_client.get = AsyncMock(return_value=FakeResponse(500, data={}))
    lat = 123.456
    lon = 789.012
    result = await client.get_weather_for_next_five_days(lat, lon)
    assert result is None


@pytest.mark.asyncio
async def test_get_lat_long_success(client, mock_http_client):
    mock_http_client.get = AsyncMock(return_value=FakeResponse(200, data=[{"data": "dummy"}]))
    city = "Test City"
    state = "Test State"
    result = await client.get_lat_long(city, state)
    assert result == [{"data": "dummy"}]


@pytest.mark.asyncio
async def test_get_lat_long_not_authorized(client, mock_http_client):
    mock_http_client.get = AsyncMock(return_value=FakeResponse(401, data={}))
    city = "Test City"
    state = "Test State"
    with pytest.raises(NotAuthorizedException):
        await client.get_lat_long(city, state)


@pytest.mark.asyncio
async def test_get_lat_long_unknown_code(client, mock_http_client):
    mock_http_client.get = AsyncMock(return_value=FakeResponse(500, data={}))
    city = "Test City"
    state = "Test State"

    lat_long = await client.get_lat_long(city, state)
    assert lat_long is None
