from lswapi import __api_base_url__
from lswapi import __auth_token_url__
from lswapi.requests.session import LeasewebSession
from lswapi.requests.session import LeasewebApiKeyAuth
from os import environ


def get_leaseweb_api(api_key=None, client_id=None, client_secret=None, base_url=None, token_url=None, token_store=None):
    base_url = base_url or environ.get("LSW_BASE_URL", __api_base_url__)
    token_url = token_url or environ.get("LSW_AUTH_URL", __auth_token_url__)
    token_store = token_store or environ.get("LSW_AUTH_TOKEN_STORE", None)
    api_key = api_key or environ.get("LSW_API_KEY")
    if api_key:
        api = LeasewebSession(base_url=base_url)
        api.auth = (LeasewebApiKeyAuth(api_key))
        return api
    client_id = client_id or environ.get("LSW_CLIENT_ID")
    client_secret = client_secret or environ.get("LSW_CLIENT_SECRET")
    if client_id and client_secret:
        return LeasewebSession(base_url=base_url, client_id=client_id, client_secret=client_secret, token_url=token_url, token_store=token_store)
    raise Exception("No authentication method specified")
