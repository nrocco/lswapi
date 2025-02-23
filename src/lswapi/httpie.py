"""
LswApi auth plugin for HTTPie.
"""
from httpie.plugins import AuthPlugin
from json import loads, dumps
from lswapi import __auth_token_url__
from lswapi.requests import fetch_access_token
from os import path
from time import time


__token_store__ = path.expanduser("~/.lswapi.token")


class LswApiAuth(object):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def __call__(self, r):
        if path.exists(__token_store__):
            with open(__token_store__, "r") as file:
                token = loads(file.read())
            if "expires_at" in token and token["expires_at"] > time():
                r.headers["Authorization"] = "{token_type} {access_token}".format(**token)
                return r

        token = fetch_access_token(__auth_token_url__, self.client_id, self.client_secret)

        with open(__token_store__, "w") as file:
            file.write(dumps(token))

        r.headers["Authorization"] = "{token_type} {access_token}".format(**token)
        return r


class ApiAuthPlugin(AuthPlugin):
    name = "LswApi Oauth"
    auth_type = "lswapi"
    description = "Leaseweb Api Oauth Authentication"

    def get_auth(self, username, password):
        return LswApiAuth(username, password)
