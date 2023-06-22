# Variables
IMAGE_NAME = tweet-app
CONTAINER_NAME = my-tweet-container
APP_PORT = 8000


# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -d --name $(CONTAINER_NAME) --rm -p $(APP_PORT):$(APP_PORT) -e WEATHER_MAP_API_KEY=$(WEATHER_MAP_API_KEY) -e TWITTER_BEARER_TOKEN=$(TWITTER_BEARER_TOKEN) -e TWITTER_CONSUMER_KEY=$(TWITTER_CONSUMER_KEY) -e TWITTER_CONSUMER_SECRET=$(TWITTER_CONSUMER_SECRET) -e TWITTER_ACCESS_TOKEN=$(TWITTER_ACCESS_TOKEN) -e TWITTER_ACCESS_TOKEN_SECRET=$(TWITTER_ACCESS_TOKEN_SECRET) $(IMAGE_NAME)


# Stop the Docker container
stop:
	docker stop $(CONTAINER_NAME)

# Remove the Docker image
clean:
	docker rmi $(IMAGE_NAME)

# Run the application
app:
	uvicorn app:app --host 0.0.0.0 --port $(APP_PORT)

# Shortcut for building the image, running the container, and starting the application
start: build run

# Help command to display available targets
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  build      Build the Docker image"
	@echo "  run        Run the Docker container"
	@echo "  stop       Stop the Docker container"
	@echo "  clean      Remove the Docker image"
	@echo "  app        Run the application locally"
	@echo "  start      Build, run, and start the application"
	@echo "  help       Display this help message"