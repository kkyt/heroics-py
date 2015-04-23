from __future__ import absolute_import

import os
import yaml

from click import group, command, argument, option, pass_context, Path

from kuankr_utils import log, debug, json, api_client, api_cli

@group()
@option('--debug', default=False, is_flag=True, help='debug mode')
@pass_context
def hr(ctx, debug):
    ctx.obj = {
        'debug': debug,
    }

@hr.command(help='call http api. METHOD: service.resource.link eg: kuankr_auth.user.info')
@option('-d', '--data')
@option('-f', '--file', type=Path(exists=True))
@option('--doc', is_flag=True)
@option('--stream', is_flag=True)
@argument('method', metavar='METHOD', default=None)
@argument('args', nargs=-1)
def api(method, args, file=None, data=None, doc=None, stream=False):
    return api_cli.run_api(method, args, file, data, doc=doc, stream=stream)

@hr.command(help='dump api schema')
@argument('service', metavar='SERVICE', default=None)
def schema(service):
    client = api_client.ApiClient(service)
    print json.dumps(client.schema, pretty=True)
    
@hr.command(help='info for api resource/link, TARGET: service or service.resource or service.resource.link')
@argument('target', metavar='TARGET', default=None)
def info(target):
    a = target.split('.')
    client = api_client.ApiClient(a[0])
    api = client.api
    if len(a)==1:
        r = api._resources.keys()
    elif len(a)==2:
        r = api._resources[a[1]]._links.keys()
    elif len(a)==3:
        r = api._resources[a[1]]._links[a[2]].schema
    else:
        raise Exception('invalid target format')
    print json.dumps(r, pretty=True)

def main():
    try:
        hr()
    except Exception as e:
        msg = debug.pretty_traceback()
        log.info('\n%s\n' % msg)

if __name__ == '__main__':
    main()

