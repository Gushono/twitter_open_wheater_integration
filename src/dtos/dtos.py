from typing import Optional

from pydantic import BaseModel


class CityInfoBody(BaseModel):
    city: str
    state: Optional[str] = ""

    class Config:
        schema_extra = {
            "example": {
                "city": "Campinas",
            }
        }


class CityLatLong(BaseModel):
    name: str
    lat: float
    long: float


class WeatherDescription(BaseModel):
    temperature: int
    weather_description: str
