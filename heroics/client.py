
import os
import sys
import json

from kuankr_api_utils.client import Client as HttpClient

def create_heroics_client(service, **options)
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
            headers['x_%s' % x] = v

    dh = options.get('default_headers')
    if dh:
        headers.update(dh)
    options['default_headers'] = headers
    return Client(schema, url, options)

class Client(object):
    def __init__(self, schema, url, options):
        self.schema = schema
        self.url = url
        self.options = options
        self.http_client = HttpClient(url, headers=options['default_headers'])

        self.resources = {}
        for s in self.client.schema['properties']:
            self.resource[s] = Resource(self, s)

    def __getattr__(self, resource):
        return self.resources[resource]


