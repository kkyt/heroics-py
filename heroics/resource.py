from __future__ import absolute_import
from .link import Link

class Resource(object):
    def __init__(self, client, name):
        self._client = client
        self._name = name
        self._links = {}

        for s in self._schema['links']:
            method = '_'.join(s['title'].lower().split())
            self._links[method] = Link(self, method, s)

    @property
    def _schema(self):
        #hack
        return self._client._schema['definitions'][self._name]

    def __getattr__(self, method):
        if method.startswith('_'):
            raise AttributeError()
        return self._links[method]


