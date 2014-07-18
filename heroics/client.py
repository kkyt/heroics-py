#coding: utf8

from __future__ import absolute_import

import os
import sys
import json

from kuankr_utils.http_client import HttpClient

from .resource import Resource

class Client(object):
    def __init__(self, schema, url, options):
        self._schema = schema
        self._url = url
        self._options = options
        self._http_client = HttpClient(url, headers=options['default_headers'])

        self._resources = {}
        for s in self._schema['properties']:
            res_name = s.replace('-','_')
            self._resources[res_name] = Resource(self, s)

    def __getattr__(self, resource):
        return self._resources[resource]


