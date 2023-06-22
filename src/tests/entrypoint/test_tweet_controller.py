from unittest import mock

import pytest

from src.dtos.dtos import CityInfoBody, CityLatLong
from src.entrypoints.controllers.v1.twitter_controller import post_weather_on_twitter
from src.exceptions.client_exceptions import TwitterSendMessageException, NotAuthorizedException

city_info_body = CityInfoBody(city="London", state="UK")
mock_get_city_lat_long = mock.AsyncMock(return_value=CityLatLong(lat=51.5074, long=-0.1278, name="London"))
mock_get_median_temperature_for_next_five_days = {
    "23/6": {"average_temp": 25, "description": "Sunny"},
    "24/6": {"average_temp": 21, "description": "Cloudy"},
    "25/6": {"average_temp": 18, "description": "Rainy"},
    "26/6": {"average_temp": 23, "description": "Sunny"},
}
mock_publish = mock.AsyncMock()


@pytest.fixture
def mock_env_variables_twitter(monkeypatch):
    monkeypatch.setenv("TWITTER_BEARER_TOKEN", "bearer_token")
    monkeypatch.setenv("TWITTER_CONSUMER_KEY", "consumer_key")
    monkeypatch.setenv("TWITTER_CONSUMER_SECRET", "consumer_secret")
    monkeypatch.setenv("TWITTER_ACCESS_TOKEN", "access_token")
    monkeypatch.setenv("TWITTER_ACCESS_TOKEN_SECRET", "access_token_secret")


@pytest.mark.asyncio
@mock.patch("src.services.search_weather_service.WeatherSearchService.get_city_lat_long",
            return_value=CityLatLong(lat=51.5074, long=-0.1278, name="London"))
@mock.patch("src.services.search_weather_service.WeatherSearchService.get_median_temperature_for_next_five_days",
            return_value=mock_get_median_temperature_for_next_five_days)
@mock.patch("src.services.social_media_service.TwitterService.publish", return_value=mock_publish)
async def test_post_weather_on_twitter(publish, median, lat_long, mock_env_variables_twitter):
    result = await post_weather_on_twitter(city_info_body)

    expected_message = "25°C e Sunny em London em 23/6. Média para os próximos dias: 21°C em 24/6, 18°C em 25/6, 23°C em 26/6."
    lat_long.assert_called_once_with(city="london", state="uk")
    median.assert_called_once_with(city_lat_long=CityLatLong(lat=51.5074, long=-0.1278, name="London"))
    publish.assert_called_once_with(message=expected_message)

    assert result == {"message": expected_message}


@pytest.mark.asyncio
@mock.patch("src.services.search_weather_service.WeatherSearchService.get_city_lat_long",
            side_effect=NotAuthorizedException)
@mock.patch("src.services.search_weather_service.WeatherSearchService.get_median_temperature_for_next_five_days",
            return_value=mock_get_median_temperature_for_next_five_days)
@mock.patch("src.services.social_media_service.TwitterService.publish", side_effect=mock_publish)
async def test_post_weather_receiving_401(publish, median, lat_long, mock_env_variables_twitter):
    with pytest.raises(Exception) as e:
        await post_weather_on_twitter(city_info_body)

    assert e.typename == 'HTTPException'
    assert e.value.status_code == 401


@pytest.mark.asyncio
@mock.patch("src.services.search_weather_service.WeatherSearchService.get_city_lat_long",
            return_value=CityLatLong(lat=51.5074, long=-0.1278, name="London"))
@mock.patch("src.services.search_weather_service.WeatherSearchService.get_median_temperature_for_next_five_days",
            return_value=mock_get_median_temperature_for_next_five_days)
@mock.patch("src.services.social_media_service.TwitterService.publish", side_effect=TwitterSendMessageException)
async def test_post_weather_receiving_422(publish, median, lat_long, mock_env_variables_twitter):
    with pytest.raises(Exception) as e:
        await post_weather_on_twitter(city_info_body)

    assert e.typename == 'HTTPException'
    assert e.value.status_code == 422


@pytest.mark.asyncio
@mock.patch("src.services.search_weather_service.WeatherSearchService.get_city_lat_long",
            side_effect=Exception)
@mock.patch("src.services.search_weather_service.WeatherSearchService.get_median_temperature_for_next_five_days",
            return_value=mock_get_median_temperature_for_next_five_days)
@mock.patch("src.services.social_media_service.TwitterService.publish", return_value=mock_publish)
async def test_post_weather_receiving_500(publish, median, lat_long, mock_env_variables_twitter):
    with pytest.raises(Exception) as e:
        await post_weather_on_twitter(city_info_body)

    assert e.typename == 'HTTPException'
    assert e.value.status_code == 500
