import os
import requests

class LswApi(object):
    base_url = 'https://api.leaseweb.com'
    token = None

    @classmethod
    def get_url(cls, uri):
        return cls.base_url + '/' + uri

    @classmethod
    def get_token(cls):
        return cls.token if cls.token else os.getenv("LSW_API_KEY")

    @classmethod
    def get(cls, uri, *args, **kwargs):
        kwargs['headers'] = {'X-Lsw-Auth': cls.get_token()}
        url = cls.get_url(uri)
        resp = requests.get(url, *args, **kwargs)
        return resp.json()


class LswApiResource(LswApi):
    @classmethod
    def all(cls, *args, **kwargs):
        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['limit'] = 1000
        data = super(LswApiResource, cls).get(cls._resource_loc, *args, **kwargs)
        return [cls(r) for r in data[cls._resource_name]]

    @classmethod
    def filter(cls, filter):
        return cls.all(params={'filter':filter})

    @classmethod
    def get(cls, id):
        data = super(LswApiResource, cls).get(cls._resource_loc + '/' + id)
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
        self._update(LswApi.get(self.uri()))

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


class BareMetal(LswApiResource):
    _resource_id = 'bareMetalId'
    _resource_name = 'bareMetals'
    _resource_loc = 'v1/bareMetals'

    def _update(self, attrs):
        super(BareMetal, self)._update(attrs['bareMetal'])

    def power_cycle(self):
        if not self.id:
            raise Exception()
        return LswApi.post(self.uri() + '/reboot')


class NetworkDevice(LswApiResource):
    _resource_id = 'name'
    _resource_name = 'networkDevices'
    _resource_loc = 'v1/nseapi/networkDevices'

    def system_info(self):
        if not self.id:
            raise Exception()
        return LswApi.get(self.uri() + '/querySystemInfo')


class Powerbar(LswApiResource):
    _resource_id = 'name'
    _resource_name = 'powerbars'
    _resource_loc = 'v1/bmapi/powerbars'


class Domain(LswApiResource):
    _resource_id = 'domain'
    _resource_name = 'domains'
    _resource_loc = 'v1/domains'

    def _update(self, attrs):
        super(Domain, self)._update(attrs['domain'])


class Ip(LswApiResource):
    _resource_id = 'ip'
    _resource_name = 'ips'
    _resource_loc = 'v1/ips'

    def _update(self, attrs):
        super(Ip, self)._update(attrs['ip'])
