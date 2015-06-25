import os
from requests import request
from requests.exceptions import RequestException


base_url = 'https://api.leaseweb.com'
token = None


class LswApiException(Exception):
    def __init__(self, response):
        self.status_code = response.status_code
        try:
            body = response.json()
            message = body.get('errorMessage', 'Unknown error occurred')
        except:
            message = 'Unknown error occurred'
        return super(LswApiException, self).__init__(message)


def get_url(uri):
    return '{}/{}'.format(base_url.rstrip('/'), uri.lstrip('/'))


def get_token():
    return token if token else os.getenv("LSW_API_KEY")


def get(uri, *args, **kwargs):
    return callapi('get', uri, *args, **kwargs)


def post(uri, *args, **kwargs):
    return callapi('post', uri, *args, **kwargs)


def put(uri, *args, **kwargs):
    return callapi('put', uri, *args, **kwargs)


def delete(uri, *args, **kwargs):
    return callapi('delete', uri, *args, **kwargs)


def callapi(method, uri, *args, **kwargs):
    token = get_token()
    url = get_url(uri)
    kwargs['headers'] = {'X-Lsw-Auth': token}

    try:
        response = request(method, url, *args, **kwargs)
        response.raise_for_status()
    except RequestException:
        raise LswApiException(response)
    else:
        return response.json()


class LswApiResource(object):
    @classmethod
    def all(cls, *args, **kwargs):
        data = get(cls._resource_loc, *args, **kwargs)
        return [cls(r) for r in data[cls._resource_name]]

    @classmethod
    def filter(cls, filter):
        return cls.all(params={'filter':filter})

    @classmethod
    def get(cls, id):
        data = get(cls._resource_loc + '/' + id)
        return cls(data)

    # @classmethod
    # def create(cls, attrs):
    #     resource = cls(attrs)
    #     resource.save()
    #     return resource

    def __init__(self, attrs=None):
        if attrs == None:
            attrs = {}
        self._attrs = {}
        self._update(attrs)
        self._initialized = True

    def __str__(self):
        return '<{}: {}>'.format(self.__class__.__name__,
                                 self._attrs.get(self._resource_id))

    def __repr__(self):
        return str(self)

    def __getattr__(self, name):
        return self._attrs[name]

    def _update(self, attrs):
        if not isinstance(attrs, dict):
            return
        for key, value in attrs.items():
            self._attrs[key] = value

    @property
    def id(self):
        return self._attrs.get(self._resource_id)

    def uri(self):
        if not self.id:
            raise Exception()
        return self._resource_loc + '/' + self.id

    def reload(self):
        self._update(get(self.uri()))

    # def save(self):
    #     if not self.id:
    #         self.create()
    #     else:
    #         self.update()

    # def create(self):
    #     pass  # not implemented yet

    # def update(self):
    #     pass  # not implemented yet

    # def destroy(self):
    #     if self.id:
    #         pass  # not implemented yet
    #     else:
    #         raise Exception()
