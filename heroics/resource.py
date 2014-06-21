
class Resource(object):
    def __init__(self, client, name):
        self.client = client
        self.name = name
        self.links = {}

        for s in self.resource.schema['links']:
            method = '_'.join(s['title'].lower().split())
            self.links[method] = Link(self, method)

    @property
    def schema(self):
        #hack
        return self.client.schema['definitions'][self.name]

    def __getattr__(self, method):
        return self.links[method]



