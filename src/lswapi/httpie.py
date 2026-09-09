"""
LswApi auth plugin for HTTPie.
"""

from hashlib import md5
from json import dumps, loads
from pathlib import Path
from time import time

from httpie.cli.definition import parser as httpie_args_parser
from httpie.plugins import AuthPlugin

from lswapi import __auth_token_url__
from lswapi.requests.oauth import fetch_access_token


class LswApiAuth:
    def __init__(self, client_id, client_secret):
        if not client_id:
            raise ValueError("client_id is required")
        self.client_id = client_id
        if not client_secret:
            raise ValueError("client_secret is required")
        self.client_secret = client_secret
        options = httpie_args_parser.args
        self.token_url = options.auth_token_url or __auth_token_url__
        hash = md5(self.token_url.encode("utf-8")).hexdigest()
        self.token_store = Path.home() / ".cache" / "httpie" / f"{hash}.json"

    def __call__(self, r):
        if self.token_store.exists():
            token = loads(self.token_store.read_text())
            if "expires_at" in token and token["expires_at"] > time():
                r.headers["Authorization"] = "{token_type} {access_token}".format(**token)
                return r

        token = fetch_access_token(self.token_url, self.client_id, self.client_secret)
        self.token_store.parent.mkdir(parents=True, exist_ok=True)
        self.token_store.write_text(dumps(token))

        r.headers["Authorization"] = "{token_type} {access_token}".format(**token)
        return r


class ApiAuthPlugin(AuthPlugin):
    name = "LswApi Oauth"
    auth_type = "lswapi"
    description = "Leaseweb Api Oauth Authentication"

    params = httpie_args_parser.add_argument_group(title="LswApi Oauth OAuth2.0 options")

    params.add_argument("--auth-token-url", default=None, metavar="LSW_AUTH_URL", help="OAuth 2.0 Token endpoint URI")

    def get_auth(self, username, password):
        return LswApiAuth(username, password)
