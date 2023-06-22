import os
from abc import ABC
from typing import Optional, List

import httpx

from src.exceptions.client_exceptions import NotAuthorizedException


class WeatherSearchClient(ABC):
    async def get_lat_long(self, city: str, state: str, limit: int = 1) -> Optional[dict]:
        raise NotImplementedError

    async def get_weather_for_next_five_days(self, lat: float, long: float) -> Optional[dict]:
        raise NotImplementedError


class OpenWeatherMapAPIClient(WeatherSearchClient):

    def __init__(self):
        self.geo_base_url = "https://api.openweathermap.org/geo/1.0/direct"
        self.data_base_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.api_key = os.getenv("WEATHER_MAP_API_KEY")

    async def get_weather_for_next_five_days(self, lat: float, long: float) -> Optional[dict]:
        params = {"lat": lat, "lon": long, "units": "metric", "lang": "pt", "appid": self.api_key}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.data_base_url, params=params)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise NotAuthorizedException()

        return None

    async def get_lat_long(self, city: str, state: str, limit: int = 5) -> Optional[List[dict]]:
        if state:
            city = f"{city},{state}"

        params = {"q": city, "limit": limit, "appid": self.api_key}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.geo_base_url, params=params)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise NotAuthorizedException()

        return None
