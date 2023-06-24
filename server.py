import os

from fastapi import FastAPI

from src.config.logger import LoggingMiddleware
from src.database.database import init_db
from src.entrypoints.routers.router import add_routes

REQUIRED_ENV_VARIABLES = [
    "WEATHER_MAP_API_KEY",
    "TWITTER_BEARER_TOKEN",
    "TWITTER_CONSUMER_KEY",
    "TWITTER_CONSUMER_SECRET",
    "TWITTER_ACCESS_TOKEN",
    "TWITTER_ACCESS_TOKEN_SECRET"
]


def validate_environment_variables():
    missing_variables = []
    for var in REQUIRED_ENV_VARIABLES:
        if var not in os.environ:
            missing_variables.append(var)

    if missing_variables:
        raise Exception(f"Missing environment variables: {missing_variables}")


def create_app(debug_mode: bool) -> FastAPI:
    validate_environment_variables()

    app = FastAPI()
    app.add_middleware(LoggingMiddleware)
    add_routes(app)
    init_db(app)

    if debug_mode:
        print(f"RUNNING ON DEBUG MODE, {debug_mode=}")
        app.debug = True

    return app
