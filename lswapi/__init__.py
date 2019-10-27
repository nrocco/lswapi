from os import environ, path
from requests.auth import AuthBase
from requests import Session
from requests import post
from time import time

__version__ = '0.4.2'
__auth_token_url__ = 'https://auth.leaseweb.com/token'
__api_base_url__ = 'https://api.leaseweb.com'
__token_store__ = path.expanduser('~/.lswapi.token')


def get_leaseweb_api(api_key=None, client_id=None, client_secret=None, base_url=None, token_url=None):
    base_url = base_url or environ.get('LSW_BASE_URL', __api_base_url__)
    token_url = token_url or environ.get('LSW_AUTH_URL', __auth_token_url__)

    api_key = api_key or environ.get('LSW_API_KEY')
    if api_key:
        api = LeaseWebSession(base_url=base_url)
        api.auth = (LeasewebApiKeyAuth(api_key))
        return api

    client_id = client_id or environ.get('LSW_CLIENT_ID')
    client_secret = client_secret or environ.get('LSW_CLIENT_SECRET')
    if client_id and client_secret:
        return LeaseWebSession(base_url=base_url, client_id=client_id, client_secret=client_secret, token_url=token_url)

    raise Exception("No authentication method specified")


def fetch_access_token(token_url, client_id, client_secret):
    response = post(token_url, auth=(client_id, client_secret), data={'grant_type': 'client_credentials'})
    if response.status_code != 200:
        raise Exception('Could not obtain an access token')
    token = response.json()
    token['created_at'] = int(time())
    token['expires_at'] = token['created_at'] + token['expires_in'] - 10
    return token


class LeasewebApiKeyAuth(AuthBase):
    def __init__(self, lsw_auth_key):
        self.lsw_auth_key = lsw_auth_key

    def __call__(self, r):
        r.headers['X-Lsw-Auth'] = self.lsw_auth_key
        return r


class LeaseWebSession(Session):
    access_token = None

    def __init__(self, client_id=None, client_secret=None, base_url=None, token_url=None):
        self.base_url = base_url or __api_base_url__
        self.token_url = token_url or __auth_token_url__
        self.client_id = client_id
        self.client_secret = client_secret
        super(LeaseWebSession, self).__init__()

    def _fetch_access_token(self):
        return fetch_access_token(self.token_url, self.client_id, self.client_secret)

    def request(self, method, url, data=None, headers={}, **kwargs):
        if self.client_id and self.client_secret:
            if not self.access_token:
                self.access_token = self._fetch_access_token()
            if int(time()) > self.access_token['expires_at']:
                self.access_token = self._fetch_access_token()  # TODO: use refresh tokens instead
            headers['Authorization'] = '{token_type} {access_token}'.format(**self.access_token)
        if not url.startswith('http'):
            url = '{}/{}'.format(self.base_url, url.lstrip('/'))

        # if response.status_code == 401 and 'WWW-Authenticate' in response.headers:
        #     pass # TODO analyse the WWW-Authenticate response header

        return super(LeaseWebSession, self).request(method, url, headers=headers, data=data, **kwargs)
