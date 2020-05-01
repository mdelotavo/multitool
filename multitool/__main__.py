#!/usr/bin/env python
# __main__.py

import re
import requests

import click

from multitool.utils import show_message

URL = 'https://en.wikipedia.org/wiki/"Hello,_World!"_program'


def do_hello():
    result = requests.get(URL)
    show_message(re.findall('<title>(.*?)</title>', result.text)[0])

@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")


if __name__ == '__main__':
    # do_hello() # pragma: no cover
    hello() # pragma: no cover
