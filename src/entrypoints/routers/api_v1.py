from fastapi import APIRouter

from src.entrypoints.controllers.v1.twitter_controller import post_weather_on_twitter

api_v1 = APIRouter(prefix="/v1")

api_v1.add_api_route(
    path="/tweet",
    endpoint=post_weather_on_twitter,
    methods=["POST"],
    response_model=dict,
    responses={
        401: {"description": "Unauthorized"},
        500: {"description": "Internal Server Error"}
    }
)
