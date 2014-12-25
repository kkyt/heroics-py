import re
import types

PARAMETER_REGEX = re.compile(r'\{\([%\/a-zA-Z0-9_-]*\)\}')

def is_generator(x):
    return isinstance(x, types.GeneratorType)

