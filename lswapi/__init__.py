__version__ = '0.2.0'
__auth_token_url__ = 'https://auth.leaseweb.com/token'
__api_base_url__ = 'https://api.leaseweb.com'
__token_store__ = '/tmp/lswapi.token'

from requests.auth import AuthBase
from requests import Session
from requests import post

def get_leaseweb_api(base_url=__api_base_url__):
    from os import environ
    if 'LSW_API_KEY' in environ:
        api = LeaseWebSession(base_url=base_url)
        api.auth = (LeasewebLegacyAuth(environ['LSW_API_KEY']))

    else:
        api = LeaseWebSession(base_url=base_url,
                              client_id=environ['LSW_CLIENT_ID'],
                              client_secret=environ['LSW_CLIENT_SECRET'])
    return api


class LeasewebLegacyAuth(AuthBase):
    def __init__(self, lsw_auth_key):
        self.lsw_auth_key = lsw_auth_key

    def __call__(self, r):
        r.headers['X-Lsw-Auth'] = self.lsw_auth_key
        return r


class LeaseWebSession(Session):
    access_token = None

    def __init__(self, client_id=None, client_secret=None, token_url=__auth_token_url__, base_url=__api_base_url__):
        self.base_url = base_url
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret

        super(LeaseWebSession, self).__init__()

    def fetch_token(self):
        response = post(self.token_url,
                        auth=(self.client_id, self.client_secret),
                        data = {'grant_type': 'client_credentials'})
        self.access_token = response.json()

    def request(self, method, url, data=None, headers={}, **kwargs):
        if self.client_id or self.client_secret:
            if not self.access_token:
                self.fetch_token()
            headers['Authorization'] = '{token_type} {access_token}'.format(**self.access_token)

        if not url.startswith('http'):
            url = '{}/{}'.format(self.base_url, url.lstrip('/'))

        return super(LeaseWebSession, self).request(method, url, headers=headers, data=data, **kwargs)
