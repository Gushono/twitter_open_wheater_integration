# Project Name: Weather Twitter Bot

## Description

The Weather Twitter Bot is a project that obtains weather information from the OpenWeatherMap API and automatically
posts it on Twitter using the Tweepy library. It fetches the current weather data for a specified location and tweets it
with relevant details such as temperature, humidity, wind speed, and weather conditions.

## Features

- Fetches current weather data from the OpenWeatherMap API.
- Authenticates with the Twitter API using Tweepy library.
- Formats the weather information into a tweet.
- Posts the weather tweet on a specified Twitter account.

## Prerequisites

- Python 3.10 or higher
- Poetry (dependency management)

## Installation

1. Clone the repository:

   ```bash
   $ https://github.com/Gushono/twitter_open_wheater_integration
   $ cd twitter_open_wheater_integration

    ```

2. Install the dependencies using Poetry:

   ```bash
    poetry install

   ```
3. Start the FastAPI server:

   ```bash
   WEATHER_MAP_API_KEY=your_weather_map_api_key TWITTER_BEARER_TOKEN=your_twitter_bearer_token TWITTER_CONSUMER_KEY=your_twitter_consumer_key TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret TWITTER_ACCESS_TOKEN=your_twitter_access_token TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret poetry run uvicorn app:app
   ```

   The server will start running on http://localhost:8000.

4. Make a POST request to /v1/tweet and you gonna receive the results.

## Usage with makefile and docker

1. You can run a command to see all available commands:

   ```
   $ make help
   ```

2. You can run a command to execute all steps of docker and run you app

   ```
   $ make start WEATHER_MAP_API_KEY=your_weather_map_api_key TWITTER_BEARER_TOKEN=your_twitter_bearer_token TWITTER_CONSUMER_KEY=your_twitter_consumer_key TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret TWITTER_ACCESS_TOKEN=your_twitter_access_token TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   ```

## Documentation

1. You can access the documentation of the API by going to http://localhost:8000/docs.

