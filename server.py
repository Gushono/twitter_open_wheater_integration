from fastapi import FastAPI

from src.database.database import init_db
from src.entrypoints.routers.router import add_routes


def create_app(debug_mode: bool) -> FastAPI:
    app = FastAPI()
    add_routes(app)
    init_db(app)

    if debug_mode:
        print(f"RUNNING ON DEBUG MODE, {debug_mode=}")
        app.debug = True

    return app
