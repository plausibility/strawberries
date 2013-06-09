# -*- coding: utf-8 -*-
import girclib.irc
import girclib.client
import girclib.signals
from functools import wraps

import strawberries
import strawberries.routing

import logging


class Bot(girclib.client.IRCClient):
    commands = []
    events = []

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        sigs = dir(girclib.signals)
        for e in [f for f in sigs if f.startswith('on_')]:
            event = getattr(girclib.signals, e)
            f = self.handle_event(e)
            event.connect(f, weak=False)

    def command(self, name, params=None, rank=0, prefix=None):
        prefix = prefix or "!"
        def outer_decorator(f):
            @wraps(f)
            def inner_decorator(*nargs, **kwargs):
                if len(nargs) == 0:
                    # Explicit "None" line for parse.
                    nargs = (None,)
                args = strawberries.routing._parse_args(params, *nargs)
                return f(**args)
            self.commands.append((name, inner_decorator, params, rank, prefix,))
            return inner_decorator
        return outer_decorator

    def event(self, event):
        def outer_decorator(f):
            self.events.append(('on_{0}'.format(event), f))
            return f
        return outer_decorator

    def handle_event(self, event):
        def decorator(*args, **kwargs):
            calling = []
            for e in self.events:
                if event != e[0]:
                    continue
                calling.append(e[1])
            # Send off those events!
            [f(*args, **kwargs) for f in calling]
        return decorator
