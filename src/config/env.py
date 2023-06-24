import os

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
