"""
LswApi auth plugin for HTTPie.
"""
from json import loads, dumps
from time import time
from os import path
from lswapi import __auth_token_url__, __token_store__, fetch_access_token
from requests import post
from httpie.plugins import AuthPlugin

class LswApiAuth(object):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def __call__(self, r):
        if path.exists(__token_store__):
            with open(__token_store__, 'r') as file:
                token = loads(file.read())
            if 'expires_at' in token and token['expires_at'] > time():
                r.headers['Authorization'] = '{token_type} {access_token}'.format(**token)
                return r

        token = fetch_access_token(self.client_id, self.client_secret, __auth_token_url__)
        token['created_at'] = time()
        token['expires_at'] = token['created_at'] + token['expires_in']

        with open(__token_store__, 'w') as file:
            file.write(dumps(token))

        r.headers['Authorization'] = '{token_type} {access_token}'.format(**token)
        return r


class ApiAuthPlugin(AuthPlugin):
    name = 'LswApi Oauth'
    auth_type = 'lswapi'
    description = 'LeaseWeb Api Oauth Authentication'

    def get_auth(self, client_id, client_secret):
        return LswApiAuth(client_id, client_secret)
