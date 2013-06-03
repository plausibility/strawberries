# -*- coding: utf-8 -*-
import girclib.irc
import girclib.client
from functools import wraps

import strawberries
import strawberries.routing


class Bot(girclib.client.BasicIRCClient):
    commands = []

    def command(self, name, params=None, defaults=None, prefix="!"):
        def outer_decorator(f):
            @wraps(f)
            def inner_decorator(*nargs, **kwargs):
                if len(nargs) == 0:
                    # Explicit "None" line for parse.
                    nargs = (None,)
                args = strawberries.routing._parse_args(params, *nargs)
                return f(**args)
            self.commands.append((name, inner_decorator,))
            return inner_decorator
        return outer_decorator
