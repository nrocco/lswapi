import logging
import time

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, debug=False) -> None:
        self.debug = debug

    async def __call__(self, method, url, next_func, **kwargs):
        start = time.monotonic()
        response = await next_func(method, url, **kwargs)
        end = time.monotonic()
        logger.info(f"Request to {response.method} {response.url} took {(end - start):.3f} seconds and resulted in a {response.status} {response.reason}")
        if self.debug:
            for header, value in response.request_info.headers.items():
                logger.debug(f">>> {header}: {value}")
            logger.debug(f"<<< HTTP/{response.version.major}.{response.version.minor} {response.status} {response.reason}")
            for header, value in response.headers.items():
                logger.debug(f"<<< {header}: {value}")
        return response
