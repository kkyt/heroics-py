import re

PARAMETER_REGEX = re.compile(r'\{\([%\/a-zA-Z0-9_-]*\)\}')

class Link(object):
    def __init__(self, resource, name, schema):
        self.resource = resource
        self.name =name
        self.schema = schema

    def format_path(self, schema, args, kwargs):
        path = schema['href']
        g = PARAMETER_REGEX.findall(path)
        n = len(g)

        if len(args) == n+1 and not kwargs and isinstance(args[-1], dict):
            args = args[:-1]
            kwargs = args[-1]

        if len(args) != n:
            raise Exception("wrong number of arguments (%s for %s)" % (len(args), n))

        for i in range(n):
            path = PARAMETER_REGEX.sub(str(args[i]), path)
        return path, kwargs

    def call(self, args, kwargs, stream=False):
        s = self.schema
        method = s['method'].lower()
        params = None
        path, body = self.format_path(s, args, kwargs)
        if method=='get' and body:
            params = body
            body = None

        r = self.resource
        c = r._client

        #h = json.dumps(c.options['default_headers'])
        #log.info('Heroics.Link.run %s %s %s' % (c.service, r.name, self.name))
        #log.info('%s %s%s %s' % (s['method'].upper(), c.url, path, h)) 
        #if body: log.debug(simple_json.pretty_dumps(body))

        r = c._http_client.http(method, path, body, params=params, stream=stream)

        #if not stream: log.debug(simple_json.pretty_dumps(r))
        return r

    def __call__(self, *args, **kwargs):
        return self.call(args, kwargs)

    def stream(self, *args, **kwargs):
        return self.call(args, kwargs, stream=True)

