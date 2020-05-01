#!/usr/bin/env python
# __main__.py

import re
import requests

import click

from multitool import APP
from multitool import __version__ as version
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

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(version, '-V', '--version')
def cli():
    pass

@cli.command()
def initdb():
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    click.echo('Dropped the database')

def main():
    cli(prog_name=APP)
    cli.add_command(initdb)
    cli.add_command(dropdb)


if __name__ == '__main__':
    # do_hello() # pragma: no cover
    # hello() # pragma: no cover
    # cli() # pragma: no cover
    main() # pragma: no cover
