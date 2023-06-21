from fastapi import APIRouter

from src.dtos.dtos import CompanyDetails
from src.entrypoints.controllers.v1.twitter_controller import post_weather_on_twitter

api_v1 = APIRouter(prefix="/v1")

api_v1.add_api_route(
    path="/tweet",
    endpoint=post_weather_on_twitter,
    methods=["POST"],
    response_model=list[CompanyDetails],
)
