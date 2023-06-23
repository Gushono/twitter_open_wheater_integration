from unittest.mock import AsyncMock

import pytest

from src.adapters.weathermap_client import WeatherSearchClient
from src.dtos.dtos import CityLatLong, WeatherDescription
from src.models.city import City
from src.services.search_weather_service import WeatherSearchService
from src.services.search_weather_service import calculate_average_temp_for_day


@pytest.fixture
def mock_weather_search_client():
    return AsyncMock(spec=WeatherSearchClient)


@pytest.fixture
def weather_search_service(mock_weather_search_client):
    return WeatherSearchService(api_client=mock_weather_search_client)


@pytest.fixture
def mock_city():
    city_data = {
        "name": "Test City",
        "state": "Test State",
        "lat": 123.45,
        "long": 67.89,
    }
    return City(**city_data)


@pytest.fixture
def mock_next_five_days_weather():
    weather_data = {
        "list": [
            {
                "dt_txt": "2023-06-23 12:00:00",
                "main": {"temp": 25},
                "weather": [{"description": "Sunny"}],
            },
            {
                "dt_txt": "2023-06-24 12:00:00",
                "main": {"temp": 20},
                "weather": [{"description": "Cloudy"}],
            },
            {
                "dt_txt": "2023-06-24 18:00:00",
                "main": {"temp": 22},
                "weather": [{"description": "Partly cloudy"}],
            },
            {
                "dt_txt": "2023-06-25 12:00:00",
                "main": {"temp": 18},
                "weather": [{"description": "Rainy"}],
            },
            {
                "dt_txt": "2023-06-26 12:00:00",
                "main": {"temp": 23},
                "weather": [{"description": "Sunny"}],
            },
        ]
    }
    return weather_data


@pytest.mark.asyncio
async def test_get_city_lat_long_existing_city(weather_search_service, mock_city, mock_weather_search_client):
    mock_weather_search_client.get_lat_long.return_value = []
    City.get_or_none = AsyncMock(return_value=mock_city)

    city = "Test City"
    state = "Test State"
    result = await weather_search_service.get_city_lat_long(city, state)

    City.get_or_none.assert_called_once_with(name=city.strip(), state=state.strip().lower())
    mock_weather_search_client.get_lat_long.assert_not_called()
    assert result == CityLatLong.parse_obj(mock_city.to_dict())


@pytest.mark.asyncio
async def test_get_city_lat_long_not_existing_city(weather_search_service, mock_city, mock_weather_search_client):
    mock_weather_search_client.get_lat_long.return_value = []
    City.get_or_none = AsyncMock(return_value=None)

    city = "Test City"
    state = "Test State"

    with pytest.raises(Exception):
        await weather_search_service.get_city_lat_long(city, state)

    City.get_or_none.assert_called_once_with(name=city.strip(), state=state.strip().lower())
    mock_weather_search_client.get_lat_long.assert_called_once()


@pytest.mark.asyncio
async def test_get_city_lat_long_new_city(weather_search_service, mock_weather_search_client):
    mock_weather_search_client.get_lat_long.return_value = [{"lat": 123.45, "lon": 67.89}]
    City.get_or_none = AsyncMock(return_value=None)
    City.save = AsyncMock()

    city = "Test City"
    state = "Test State"
    result = await weather_search_service.get_city_lat_long(city, state)

    City.get_or_none.assert_called_once_with(name=city.strip(), state=state.strip().lower())
    mock_weather_search_client.get_lat_long.assert_called_once_with(city=city, state=state)
    City.save.assert_called_once()
    assert result == CityLatLong.parse_obj({"name": city, "state": state, "lat": 123.45, "long": 67.89})


@pytest.mark.asyncio
def test_calculate_average_temp_for_day():
    weather_description = [
        WeatherDescription(temperature=25, weather_description="Sunny"),
        WeatherDescription(temperature=20, weather_description="Cloudy"),
        WeatherDescription(temperature=22, weather_description="Partly cloudy"),
    ]
    expected_average_temp = 22

    average_temp = calculate_average_temp_for_day(weather_description)

    assert average_temp == expected_average_temp


@pytest.mark.asyncio
async def test_group_temperatures_for_next_five_days():
    weathers = [
        {"dt_txt": "2023-06-23 12:00:00", "main": {"temp": 25}, "weather": [{"description": "Sunny"}]},
        {"dt_txt": "2023-06-24 12:00:00", "main": {"temp": 20}, "weather": [{"description": "Cloudy"}]},
        {"dt_txt": "2023-06-24 18:00:00", "main": {"temp": 22}, "weather": [{"description": "Partly cloudy"}]},
        {"dt_txt": "2023-06-25 12:00:00", "main": {"temp": 18}, "weather": [{"description": "Rainy"}]},
        {"dt_txt": "2023-06-26 12:00:00", "main": {"temp": 23}, "weather": [{"description": "Sunny"}]},
    ]
    expected_grouped_temperatures = {
        "23/6": [
            WeatherDescription(temperature=25, weather_description="Sunny")
        ],
        "24/6": [
            WeatherDescription(temperature=20, weather_description="Cloudy"),
            WeatherDescription(temperature=22, weather_description="Partly cloudy")
        ],
        "25/6": [
            WeatherDescription(temperature=18, weather_description="Rainy")
        ],
        "26/6": [
            WeatherDescription(temperature=23, weather_description="Sunny")
        ],
    }

    grouped_temperatures = await WeatherSearchService._group_temperatures_for_next_five_days(weathers)

    assert grouped_temperatures == expected_grouped_temperatures


@pytest.mark.asyncio
async def test_get_median_temperature_for_next_five_days(weather_search_service, mock_next_five_days_weather,
                                                         mock_weather_search_client, mock_city):
    mock_weather_search_client.get_weather_for_next_five_days.return_value = mock_next_five_days_weather
    weather_search_service._group_temperatures_for_next_five_days = AsyncMock(
        return_value={
            "23/6": [WeatherDescription(temperature=25, weather_description="Sunny")],
            "24/6": [
                WeatherDescription(temperature=20, weather_description="Cloudy"),
                WeatherDescription(temperature=22, weather_description="Partly cloudy")
            ],
            "25/6": [WeatherDescription(temperature=18, weather_description="Rainy")],
            "26/6": [WeatherDescription(temperature=23, weather_description="Sunny")],
        }
    )

    city_lat_long = CityLatLong.parse_obj(mock_city.to_dict())
    expected_weather_information = {
        "23/6": {"average_temp": 25, "description": "Sunny"},
        "24/6": {"average_temp": 21, "description": "Cloudy"},
        "25/6": {"average_temp": 18, "description": "Rainy"},
        "26/6": {"average_temp": 23, "description": "Sunny"},
    }

    result = await weather_search_service.get_median_temperature_for_next_five_days(city_lat_long)

    mock_weather_search_client.get_weather_for_next_five_days.assert_called_once_with(
        lat=city_lat_long.lat,
        long=city_lat_long.long
    )
    weather_search_service._group_temperatures_for_next_five_days.assert_called_once_with(
        weathers=mock_next_five_days_weather["list"]
    )
    assert result == expected_weather_information
