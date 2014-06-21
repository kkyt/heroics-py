import commandr

from pyutils import log, debug, env_utils

mod = 'heroics'
env = env_utils.Env(mod)

@commandr.command
def run(url=None):
    #TODO
    print url

def main():
    try:
        commandr.Run()
    except:
        print debug.pretty_traceback()


