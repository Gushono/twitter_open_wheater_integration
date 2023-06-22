from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


def init_db(app: FastAPI) -> None:
    Tortoise.init_models(["src.models.city"], "models")
    register_tortoise(
        app,
        db_url=f"sqlite://test.db",
        modules={"models": [
            "src.models.city",
        ]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
