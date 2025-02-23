from json import load, dump
from lswapi import __api_base_url__
from lswapi import __auth_token_url__
from lswapi.requests.oauth import fetch_access_token
from os import path
from requests import Session
from requests.auth import AuthBase
from time import time


class LeasewebApiKeyAuth(AuthBase):
    def __init__(self, lsw_auth_key):
        self.lsw_auth_key = lsw_auth_key

    def __call__(self, r):
        r.headers["X-Lsw-Auth"] = self.lsw_auth_key
        return r


class LeasewebSession(Session):
    access_token = None

    def __init__(self, client_id=None, client_secret=None, base_url=None, token_url=None, token_store=None):
        self.base_url = base_url or __api_base_url__
        self.token_url = token_url or __auth_token_url__
        self.token_store = token_store
        self.client_id = client_id
        self.client_secret = client_secret
        super().__init__()

    def _fetch_access_token(self):
        if not self.access_token and self.token_store:
            if path.exists(self.token_store):
                with open(self.token_store, "r") as file:
                    self.access_token = load(file)
        if self.access_token and self.access_token.get("expires_at") > time():
            return self.access_token
        self.access_token = fetch_access_token(self.token_url, self.client_id, self.client_secret)
        if self.token_store:
            with open(self.token_store, "w") as file:
                dump(self.access_token, file)
        return self.access_token

    def request(self, method, url, data=None, headers={}, **kwargs):
        if self.client_id and self.client_secret:
            headers["Authorization"] = "{token_type} {access_token}".format(**self._fetch_access_token())
        if not url.startswith("http"):
            url = "{}/{}".format(self.base_url, url.lstrip("/"))
        return super().request(method, url, headers=headers, data=data, **kwargs)
