#coding: utf8

from __future__ import absolute_import

import os
import sys
import json

from kuankr_api_utils.client import Client as HttpClient

from .resource import Resource

def create_heroics_client(service, **options):
    env = os.environ

    url = env['%s_URI' % service.upper()]
    schema = env['%s_SCHEMA' % service.upper()]
    f = open(schema)
    schema = json.loads(f.read())
    f.close()

    #schema = Heroics::Schema.new schema
    headers = {}
    for x in ['api_client', 'auth_token', 'admin_token']:
        v = env.get('KUANKR_%s' % x.upper())
        if v:
            h = ('x_%s' % x).replace('_', '-')
            headers[h] = v

    dh = options.get('default_headers')
    if dh:
        headers.update(dh)
    options['default_headers'] = headers
    return Client(schema, url, options)

class Client(object):
    def __init__(self, schema, url, options):
        self._schema = schema
        self._url = url
        self._options = options
        self._http_client = HttpClient(url, headers=options['default_headers'])

        self._resources = {}
        for s in self._schema['properties']:
            self._resources[s] = Resource(self, s)

    def __getattr__(self, resource):
        return self._resources[resource]


