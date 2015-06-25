from lswapi import api


class BareMetal(api.LswApiResource):
    _resource_id = 'bareMetalId'
    _resource_name = 'bareMetals'
    _resource_loc = 'v1/bareMetals'

    def _update(self, attrs):
        super(BareMetal, self)._update(attrs['bareMetal'])

    def power_status(self):
        if not self.id:
            raise Exception('You can only do this on existing resources.')
        return api.get(self.uri() + '/powerStatus')

    def power_cycle(self):
        if not self.id:
            raise Exception('You can only do this on existing resources.')
        return api.post(self.uri() + '/reboot')

    def leases(self):
        try:
            return api.get(self.uri() + '/leases')
        except api.LswApiException as e:
            if e.status_code == 404:
                return []
            else:
                raise e

    def create_lease(self, bootfile):
        return api.post(self.uri() + '/leases', data={'bootFileName':bootfile})


class NetworkDevice(api.LswApiResource):
    _resource_id = 'name'
    _resource_name = 'networkDevices'
    _resource_loc = 'v1/nseapi/networkDevices'

    def system_info(self):
        if not self.id:
            raise Exception('You can only do this on existing resources.')
        return api.get(self.uri() + '/querySystemInfo')


class Powerbar(api.LswApiResource):
    _resource_id = 'name'
    _resource_name = 'powerbars'
    _resource_loc = 'v1/bmapi/powerbars'


class Domain(api.LswApiResource):
    _resource_id = 'domain'
    _resource_name = 'domains'
    _resource_loc = 'v1/domains'

    def _update(self, attrs):
        super(Domain, self)._update(attrs['domain'])


class Ip(api.LswApiResource):
    _resource_id = 'ip'
    _resource_name = 'ips'
    _resource_loc = 'v1/ips'

    def _update(self, attrs):
        super(Ip, self)._update(attrs['ip'])

    def null(self):
        if not self.id:
            raise Exception('You can only do this on existing resources.')
        data = api.put(self.uri(), data={'nullRouted': 1})
        self._update(data)

    def unnull(self):
        if not self.id:
            raise Exception('You can only do this on existing resources.')
        data = api.put(self.uri(), data={'nullRouted': 0})
        self._update(data)

    def reverse_lookup(self, name):
        if not self.id:
            raise Exception('You can only do this on existing resources.')
        data = api.put(self.uri(), data={'reverseLookup': name})
        self._update(data)

    def get_server(self):
        if not self.serverId:
            return None
        return BareMetal.get(self.serverId)
