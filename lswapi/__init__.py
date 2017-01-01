from os import environ, path
from requests.auth import AuthBase
from requests import Session
from requests import post

__version__ = '0.3.4'
__auth_token_url__ = 'https://auth.leaseweb.com/token'
__api_base_url__ = 'https://api.leaseweb.com'
__token_store__ = path.expanduser('~/.lswapi.token')

def get_leaseweb_api(api_key=None, client_id=None, client_secret=None, base_url=__api_base_url__, token_url=__auth_token_url__):
    api_key = api_key or environ.get('LSW_API_KEY')
    client_id = client_id or environ.get('LSW_CLIENT_ID')
    client_secret = client_secret or environ.get('LSW_CLIENT_SECRET')

    if api_key:
        api = LeaseWebSession(base_url=base_url)
        api.auth = (LeasewebApiKeyAuth(api_key))
    elif client_id and client_secret:
        api = LeaseWebSession(base_url=base_url,
                              client_id=client_id,
                              client_secret=client_secret,
                              token_url=token_url)
    else:
        raise Exception("No authentication method specified")

    return api


def fetch_access_token(client_id, client_secret, token_url=__auth_token_url__):
    response = post(token_url,
                    auth=(client_id, client_secret),
                    data = {'grant_type': 'client_credentials'})
    return response.json()


class LeasewebApiKeyAuth(AuthBase):
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

    def request(self, method, url, data=None, headers={}, **kwargs):
        if self.client_id and self.client_secret:
            if not self.access_token:
                self.access_token = fetch_access_token(self.client_id,
                                                       self.client_secret,
                                                       self.token_url)
            headers['Authorization'] = '{token_type} {access_token}'.format(**self.access_token)

        if not url.startswith('http'):
            url = '{}/{}'.format(self.base_url, url.lstrip('/'))

        return super(LeaseWebSession, self).request(method, url, headers=headers, data=data, **kwargs)
