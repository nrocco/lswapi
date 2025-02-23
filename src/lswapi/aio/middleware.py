import time
import logging


class LoggingMiddleware:
    def __init__(self, debug=False) -> None:
        self.debug = debug

    async def __call__(self, method, url, next_func, **kwargs):
        start = time.monotonic()
        response = await next_func(method, url, **kwargs)
        end = time.monotonic()
        logging.info(f"Request to {response.method} {response.url} took {(end - start):.3f} seconds and resulted in a {response.status} {response.reason}")
        if self.debug:
            for header, value in response.request_info.headers.items():
                logging.debug(f">>> {header}: {value}")
            logging.debug(f"<<< HTTP/{response.version.major}.{response.version.minor} {response.status} {response.reason}")
            for header, value in response.headers.items():
                logging.debug(f"<<< {header}: {value}")
        return response
