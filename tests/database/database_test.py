from unittest import mock

from fastapi import FastAPI

from src.database.database import init_db


@mock.patch("src.database.database.Tortoise.init_models")
def test_init_db(mock_tortoise_init_models):
    app = FastAPI()
    init_db(app)

    mock_tortoise_init_models.assert_called_once_with(["src.models.city"], "models")
