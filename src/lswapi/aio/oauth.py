import aiohttp
import asyncio
import json
import os
import time

from lswapi.aio.client import LeasewebHttpClient
from lswapi.aio.middleware import LoggingMiddleware


class AccessTokenInMemoryStore:
    def __init__(self):
        self.token = None

    async def load(self):
        return self.token

    async def save(self, token):
        self.token = token

    async def remove(self):
        self.token = None


class AccessTokenFileStore:
    def __init__(self, filepath):
        self.token = None
        self.filepath = filepath
        self.lock = asyncio.Lock()

    async def load(self):
        async with self.lock:
            if self.token:
                return self.token
            if not os.path.exists(self.filepath):
                return None
            with open(self.filepath, "r") as file:
                try:
                    self.token = json.load(file)
                except json.decoder.JSONDecodeError:
                    os.remove(self.filepath)
        return self.token

    async def save(self, token):
        async with self.lock:
            with open(self.filepath, "w") as file:
                json.dump(token, file)
            self.token = token

    async def remove(self):
        async with self.lock:
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
            self.token = None


class LeasewebOAuthMiddleware:
    def __init__(self, client_id, client_secret, token_url, store=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.store = store or AccessTokenInMemoryStore()
        self.lock = asyncio.Lock()

    async def __call__(self, method, url, next_func, **kwargs):
        async with self.lock:
            token = await self.store.load()
            if not token or token.get("expires_at") < time.time():
                token = await self.__fetch_access_token()
                await self.store.save(token)
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = "{token_type} {access_token}".format(**token)
        return await next_func(method, url, **kwargs)

    async def __fetch_access_token(self):
        auth = aiohttp.BasicAuth(login=self.client_id, password=self.client_secret)
        async with LeasewebHttpClient(auth=auth, middlewares=[LoggingMiddleware(debug=False)]) as client:
            payload = {"grant_type": "client_credentials"}
            response = await client.post(self.token_url, data=payload)
            assert response.status == 200
            token = await response.json()
            token["issued_at"] = int(time.time())
            token["expires_at"] = token["issued_at"] + token["expires_in"] - 10
            return token
