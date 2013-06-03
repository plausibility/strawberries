# -*- coding: utf-8 -*-
import re

param_re = re.compile(r'''
    (?:<|\()
    (?:
        (?P<converter>[a-zA-Z_][a-zA-Z0-9_]*) # converter name
        \:                                    # variable delimiter
    )?
    (?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)      # variable name
    (?:>|\))
''', re.VERBOSE)

_CONVERTERS = {
    "default": str,
    "int": int,
    "float": float
}

def _parse_param_line(regex, line):
    """ Parses a line of parameters into a list.

        :regex: the regex we're using to parse
        :line: the parameter list, in the format ``<converter:name>``,
            where ``converter`` is one of ``int``, ``float`` and ``str``.
            Should it be ommitted (as it's optional), the default (``str``)
            will be used instead.
            You can use ``(converter:name)`` to represent an optional param,
            but this isn't definitive, you actually declare optional params as
            x=default (e.g. ``name=None``) in your function.
    """
    out = []
    for r in regex.findall(line):
        converter, variable = r[0] or 'default', r[1]
        out.append((_CONVERTERS[converter], variable))
    return out

def _parse_args(params, line=None, sep=" ", regex=None):
    if line is None:
        # For commands with nil param/args.
        return {}
    regex = regex or param_re
    func_args = {}
    param_line = _parse_param_line(regex, params)
    for i, part in enumerate(line.split(sep)):
        converter, name = param_line[i]
        func_args[name] = converter(part)
    return func_args

def parse_and_call(func, params, line, regex=None):
    """
        FOR EXAMPLE:
        :func: callable with signature: func(name=None, rank=None)
        :params: string like: '<name> <int:rank>'
        :line: user input like: 'John 3'
        :regex: a regex to parse out the arguments
    """
    regex = regex or param_re
    d = _parse_args(regex, params, line)
    return func(**d)