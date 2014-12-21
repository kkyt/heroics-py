#coding: utf8

from __future__ import absolute_import

import os
import sys
import json

from kuankr_utils.http_client import HttpClient

from .resource import Resource

def normalize_headers(h):
    #If you do not explicitly set underscores_in_headers on; 
    #nginx will silently drop HTTP headers with underscores
    #(which are perfectly valid according to the HTTP standard). 
    #This is done in order to prevent ambiguities when mapping headers to CGI variables, as both dashes and underscores are mapped to underscores during that process.
    r = {}
    for k, v in h.items():
        r[k.replace('_','-')] = v
    return r

class Client(object):
    def __init__(self, schema, url, options):
        self._schema = schema
        self._url = url
        self._options = options
        opts = {
            'headers': normalize_headers(options['default_headers']), 
            'content_type': options.get('content_type'),
            'async_send': options.get('async_send', False)
        }
        self._http_client = HttpClient(url, **opts)

        self._resources = {}
        for s in self._schema['properties']:
            res_name = s.replace('-','_')
            self._resources[res_name] = Resource(self, s)

    def __getattr__(self, resource):
        if resource.startswith('_'):
            raise AttributeError()
        return self._resources[resource]


