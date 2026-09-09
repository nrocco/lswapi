from time import time

from requests import post


def fetch_access_token(token_url, client_id, client_secret):
    response = post(token_url, auth=(client_id, client_secret), data={"grant_type": "client_credentials"})
    if response.status_code != 200:
        raise RuntimeError("Could not obtain an access token")
    token = response.json()
    token["created_at"] = int(time())
    token["expires_at"] = token["created_at"] + token["expires_in"] - 10
    return token
