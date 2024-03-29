import builtins
import http.client as http_client
import logging

import click


def verbose_callback(ctx, param, value):
    builtins.MULTITOOL_TOGGLE_VERBOSE = value
    http_client.HTTPConnection.debuglevel = value
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)


def common_verbose_options(func):
    func = click.option(
        '-v',
        '--verbose',
        show_default='toggle verbose output',
        count=True,
        callback=verbose_callback,
    )(func)
    return func
