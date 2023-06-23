from datetime import datetime
from typing import Optional

from src.adapters.weathermap_client import (OpenWeatherMapAPIClient,
                                            WeatherSearchClient)
from src.dtos.dtos import CityLatLong, WeatherDescription
from src.exceptions.search_weather_service_exceptions import \
    WeatherSearchException
from src.models.city import City


class WeatherSearchService:
    def __init__(self, api_client: WeatherSearchClient = None):
        self.api_client = api_client or OpenWeatherMapAPIClient()

    async def get_city_lat_long(self, city: str, state: str) -> CityLatLong:
        city_model = await City().get_or_none(name=city, state=state)

        if city_model:
            return CityLatLong.parse_obj(city_model.to_dict())

        response = await self.api_client.get_lat_long(city=city, state=state)

        if not response:
            raise WeatherSearchException("Error getting city lat long")

        city_model = City(
            name=city,
            state=state,
            lat=response[0]["lat"],
            long=response[0]["lon"],
        )
        await city_model.save()

        return CityLatLong.parse_obj(city_model.to_dict())

    async def get_median_temperature_for_next_five_days(
        self, city_lat_long: CityLatLong
    ) -> Optional[dict]:
        next_five_days_weather = await self.api_client.get_weather_for_next_five_days(
            lat=city_lat_long.lat, long=city_lat_long.long
        )

        grouped_temperatures = await self._group_temperatures_for_next_five_days(
            weathers=next_five_days_weather["list"]
        )

        weather_information = {}
        for day_month_key, weather_description in grouped_temperatures.items():
            weather_information[day_month_key] = {
                "average_temp": self.calculate_average_temp_for_day(
                    weather_description
                ),
                "description": weather_description[0].weather_description,
            }

        return weather_information

    @staticmethod
    def calculate_average_temp_for_day(
        weather_description: list[WeatherDescription],
    ) -> float:
        temperatures = [description.temperature for description in weather_description]
        return sum(temperatures) / len(temperatures)

    @staticmethod
    async def _group_temperatures_for_next_five_days(
        weathers: list[dict],
    ) -> dict[str, list[WeatherDescription]]:
        grouped_temperatures = {}

        for weather in weathers:
            dt = datetime.strptime(weather["dt_txt"], "%Y-%m-%d %H:%M:%S")
            day_month_key = f"{dt.day}/{dt.month}"

            weather_description = WeatherDescription(
                temperature=weather["main"]["temp"],
                weather_description=weather["weather"][0]["description"],
            )

            grouped_temperatures.setdefault(day_month_key, []).append(
                weather_description
            )

        return grouped_temperatures
