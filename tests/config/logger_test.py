import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from src.config.logger import LoggingMiddleware


@pytest.mark.asyncio
async def test_logging_middleware():
    app = FastAPI()

    app.add_middleware(LoggingMiddleware)

    @app.get("/api/test")
    async def endpoint_test():
        return {"message": "Hello, World!"}

    client = TestClient(app)

    response = client.get("/api/test")
    assert response.status_code == 200
