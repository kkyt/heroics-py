import re
import requests

from kuankr_utils import log, debug

from .utils import PARAMETER_REGEX, is_generator

class Link(object):
    def __init__(self, resource, name, schema):
        self.resource = resource
        self.name =name
        self.schema = schema

    def _to_url_param(self, v):
        m = self._to_url_param
        if isinstance(v, bool):
            if v==True:
                v = '1'
            else:
                v = '0'

        elif isinstance(v, list):
            v = ','.join([m(x) for x in v])

        #TODO?
        elif isinstance(v, dict):
            kv = ['%s:%s' % (m(k), m(v)) for k,v in v.items()]
            v = ','.join(kv)

        else:
            v = str(v)

        return v

    def _format_path(self, method, schema, args, kwargs):
        path = schema['href']
        g = PARAMETER_REGEX.findall(path)
        n = len(g)

        #body is a generator
        if len(args) == n+1:
            body = args[-1]
            args = args[:-1]
            params = kwargs
            #NOTE:
            #convert true/false params to 1/0
            for k,v in params.items():
                params[k] = self._to_url_param(v)
        elif method=='get':
            body = None
            params = kwargs
        else:
            body = kwargs
            params = None

        if len(args) != n:
            raise Exception("wrong number of arguments (%s for %s)" % (len(args), n))

        for i in range(n):
            path = PARAMETER_REGEX.sub(str(args[i]), path, count=1)
        return path, body, params

    def _get_method(self):
        return self.schema['method'].lower()

    def call(self, args, kwargs, stream=False, content_type=None, headers=None):
        s = self.schema
        method = self._get_method()
        path, body, params = self._format_path(method, s, args, kwargs)

        r = self.resource
        c = r._client

        r = c._http_client.http(method, path, body, params=params, stream=stream, content_type=content_type, headers=headers)

        return r

    def __call__(self, *args, **kwargs):
        try:
            return self.call(args, kwargs)
        except requests.HTTPError as e:
            if e.response.status_code==404 and self._get_method()=='get':
                return None
            else:
                log.error(e.response.content)
                raise

    def binary(self, *args, **kwargs):
        return self.call(args, kwargs, content_type='application/octet-stream')

    def binary_stream(self, *args, **kwargs):
        return self.call(args, kwargs, content_type='application/octet-stream', stream=True)


    def msgpack(self, *args, **kwargs):
        return self.call(args, kwargs, content_type='application/msgpack')

    def msgpack_stream(self, *args, **kwargs):
        return self.call(args, kwargs, content_type='application/msgpack', stream=True)

    #TODO: remove
    def stream(self, *args, **kwargs):
        log.error('to be removed')
        return self.call(args, kwargs, stream=True)

    def as_stream(self, *args, **kwargs):
        return self.call(args, kwargs, stream=True)

