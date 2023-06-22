# Use the official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the poetry.lock and pyproject.toml files
COPY poetry.lock pyproject.toml ./

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi


# Copy the rest of the application code
COPY . .

## Set the environment variables
ENV WEATHER_MAP_API_KEY=your_weather_map_api_key \
    TWITTER_BEARER_TOKEN=your_twitter_bearer_token \
    TWITTER_CONSUMER_KEY=your_twitter_consumer_key \
    TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret \
    TWITTER_ACCESS_TOKEN=your_twitter_access_token \
    TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Expose the port that FastAPI will be running on
EXPOSE 8000



# Run the application
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]