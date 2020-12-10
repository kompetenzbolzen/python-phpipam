from .backend import phpipamBackend

resource_types = {
    'sections' : {
        'getSubnets':{
            'method':'GET',
            'request':'/sections/{object_id}/subnets',
        }
    },
    'subnets' : {
        'search':{
            'method':'GET',
            'request':'/subnets/search/{search}'
        },
        'getIP':{
            'method':'GET',
            'requests':'/subnets/'
        }
    },
    'addresses' : {
    },
    'devices' : {
    },
}

class invalidResourceException(Exception):
    pass

class invalidResourceOperationException(Exception):
    pass

class phpipamResourceFunction:
    def __init__(self, backend, resource, function):
        if not function in resource_types[resource]:
            raise invalidResourceOperationException(f'Operation {function} is not defined for {resource}.')

        self._backend = backend
        self._resource = resource
        self._function = resource_types[resource][function]

    def __call__(self, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']
        else:
            data = {}

        return self._backend.request( self._function['method'], self._function['request'].format(**kwargs), data=data )

class phpipamResource:
    def __init__(self, backend, resource):
        if not resource in resource_types:
            raise invalidResourceException(f'Invalid resource "{resource}"')

        self._type = resource
        self._backend = backend

    def __getattr__(self, attr):
        return phpipamResourceFunction(self._backend, self._type, attr)

    def get(self):
        """List of all objects"""
        return self._backend.request('GET', f'/{self._type}')

    def byID(self, object_id):
        """object identified by object_id : str"""
        return self._backend.request('GET', f'/{self._type}/{object_id}')
