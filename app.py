import os

import uvicorn
from tortoise import Tortoise

from server import create_app

ENVIRONMENT = "development" if os.environ.get("PORT") is None else "production"
DEBUG = ENVIRONMENT == "development"

app = create_app(debug_mode=DEBUG)


@app.on_event("startup")
async def startup():
    # Generate the database schema
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
