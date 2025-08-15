from aiohttp import ClientSession


class LeasewebHttpClient:
    def __init__(self, *args, middlewares: list[callable] = [], **kwargs):
        self.middlewares = middlewares
        self.__create_session = lambda: ClientSession(*args, **kwargs)
        self.session = None

    async def _run_middlewares(self, method, url, next_func, **kwargs):
        async def middleware_chain(index, method, url, **kwargs):
            if index < len(self.middlewares):
                return await self.middlewares[index](
                    method, url, lambda m, u, **k: middleware_chain(index + 1, m, u, **k), **kwargs
                )
            return await next_func(method, url, **kwargs)
        return await middleware_chain(0, method, url, **kwargs)

    async def _request(self, method, url, **kwargs):
        if not self.session:
            self.session = self.__create_session()
        return await self.session.request(method, url, **kwargs)

    async def request(self, method, url, **kwargs):
        return await self._run_middlewares(method, url, self._request, **kwargs)

    async def get(self, url, **kwargs):
        return await self.request("GET", url, **kwargs)

    async def post(self, url, **kwargs):
        return await self.request("POST", url, **kwargs)

    async def put(self, url, **kwargs):
        return await self.request("PUT", url, **kwargs)

    async def patch(self, url, **kwargs):
        return await self.request("PATCH", url, **kwargs)

    async def delete(self, url, **kwargs):
        return await self.request("DELETE", url, **kwargs)

    async def close(self):
        if self.session:
            await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
