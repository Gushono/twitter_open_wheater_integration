import logging

from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Log the incoming request
        logger.info(f"Incoming request: {request.method} {request.url.path}")

        response = await call_next(request)

        # Log the outgoing response
        logger.info(f"Outgoing response: {response.status_code}")

        return response
