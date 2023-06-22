import os
from abc import ABC
from typing import Optional, List

import httpx

from src.exceptions.client_exceptions import NotAuthorizedException


class WeatherSearchClient(ABC):
    async def get_lat_long(self, city: str, state: str, limit: int = 1) -> Optional[dict]:  # pragma: no cover
        raise NotImplementedError

    async def get_weather_for_next_five_days(self, lat: float, long: float) -> Optional[dict]:  # pragma: no cover
        raise NotImplementedError


class OpenWeatherMapAPIClient(WeatherSearchClient):

    def __init__(self, http_client: httpx.AsyncClient = None):
        self.geo_base_url = "https://api.openweathermap.org/geo/1.0/direct"
        self.data_base_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.api_key = os.getenv("WEATHER_MAP_API_KEY")
        self.http_client = http_client or httpx.AsyncClient()

    async def get_weather_for_next_five_days(self, lat: float, long: float) -> Optional[dict]:
        params = {"lat": lat, "lon": long, "units": "metric", "lang": "pt", "appid": self.api_key}
        response = await self._get(self.data_base_url, params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise NotAuthorizedException()

        return None

    async def get_lat_long(self, city: str, state: str, limit: int = 5) -> Optional[List[dict]]:
        if state:
            city = f"{city},{state}"

        params = {"q": city, "limit": limit, "appid": self.api_key}
        response = await self._get(self.geo_base_url, params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise NotAuthorizedException()

        return None

    async def _get(self, url: str, params: dict) -> httpx.Response:
        return await self.http_client.get(url, params=params)
