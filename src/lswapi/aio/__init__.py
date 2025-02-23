from lswapi import __api_base_url__
from lswapi import __auth_token_url__
from lswapi.aio.client import LeasewebHttpClient
from lswapi.aio.middleware import LoggingMiddleware
from lswapi.aio.oauth import AccessTokenFileStore
from lswapi.aio.oauth import LeasewebOAuthMiddleware
from os import environ


def get_leaseweb_api(api_key=None, client_id=None, client_secret=None, base_url=None, token_url=None, token_store=None):
    base_url = base_url or environ.get("LSW_BASE_URL", __api_base_url__)
    token_url = token_url or environ.get("LSW_AUTH_URL", __auth_token_url__)
    token_store = token_store or environ.get("LSW_AUTH_TOKEN_STORE")
    api_key = api_key or environ.get("LSW_API_KEY")
    if api_key:
        return LeasewebHttpClient(base_url, middlewares=[LoggingMiddleware(debug=False)], headers={"X-Lsw-Auth": api_key})
    if not client_id or not client_secret:
        raise Exception("No authentication method specified")
    return LeasewebHttpClient(base_url, middlewares=[
        LeasewebOAuthMiddleware(
            client_id,
            client_secret,
            token_url,
            store=AccessTokenFileStore(token_store) if token_store else None,
        ),
        LoggingMiddleware(debug=False),
    ])
