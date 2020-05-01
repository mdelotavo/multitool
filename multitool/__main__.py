#!/usr/bin/env python
# __main__.py

import codecs
import os
import re
import requests
import sys

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

class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))

@click.group(context_settings=dict(help_option_names=["-h", "--help"]), cls=AliasedGroup)
@click.version_option(version, '-V', '--version')
# @click.command(cls=AliasedGroup)
def cli():
    pass

@cli.command()
def initdb():
    click.echo('Initialized the database')

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@cli.command()
# @click.option('--yes', is_flag=True, callback=abort_if_false,
#               expose_value=False,
#               prompt='Are you sure you want to drop the db?')
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def dropdb():
    click.echo('Dropped the database')

@cli.command()
@click.argument('string', nargs=1)
def parse_str(string):
    click.echo(string)

@cli.command()
@click.argument('integer', nargs=1, type=click.INT)
def parse_int(integer):
    click.echo(integer)

@cli.command()
@click.argument('float', nargs=1, type=click.FLOAT)
def parse_float(float):
    click.echo(float)

@cli.command()
@click.argument('bool', nargs=1, type=click.BOOL)
def parse_bool(bool):
    click.echo(bool)

@cli.command()
@click.argument('uuid', nargs=1, type=click.UUID)
def parse_uuid(uuid):#try 12345678-1234-5678-1234-567812345678
    click.echo(uuid)

@cli.command()
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def inout(input, output):
    """Copy contents of INPUT to OUTPUT."""
    while True:
        chunk = input.read(1024)
        if not chunk:
            break
        output.write(chunk)

@cli.command()
@click.argument('filename', type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=False))
def touch(filename):
    """Print FILENAME if the file exists."""
    click.echo(click.format_filename(filename))

@cli.command()
@click.option('--hash-type',
              type=click.Choice(['MD5', 'SHA1'], case_sensitive=False), default='SHA1', show_default=True)
def digest(hash_type):
    click.echo(hash_type)

@cli.command()
@click.option('--count', type=click.IntRange(0, 20, clamp=True), required=True)
@click.option('--digit', type=click.IntRange(0, 10), required=True)
def repeat(count, digit):
    click.echo(str(digit) * count)

@cli.command()
@click.option('--count', type=click.IntRange(0, 20, clamp=True), required=True)
@click.option('--float', type=click.FloatRange(0, 10), required=True)
def repeat_float(count, float):
    click.echo(str(float) * count)

@cli.command()
@click.argument('datetime', nargs=1, type=click.DateTime())
def parse_datetime(datetime):
    click.echo(datetime)

class BasedIntParamType(click.ParamType):
    name = "integer"

    def convert(self, value, param, ctx):
        try:
            if value[:2].lower() == "0x":
                return int(value[2:], 16)
            elif value[:1] == "0":
                return int(value, 8)
            return int(value, 10)
        except TypeError:
            self.fail(
                "expected string for int() conversion, got "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )
        except ValueError:
            self.fail(f"{value!r} is not a valid integer", param, ctx)

# BASED_INT = BasedIntParamType()

@cli.command()
@click.argument('string', nargs=1, type=BasedIntParamType())
def convert(string):
    click.echo(string)

@cli.command()
@click.option('--item', type=(str, int))
# @click.option('--item', nargs=2, type=click.Tuple([str, int]))
def putitem(item):
    click.echo('name=%s id=%d' % item)

@cli.command()
@click.option('--message', '-m', multiple=True, default=["foo", "bar"], show_default=True)
def commit(message):
    click.echo('\n'.join(message))

@cli.command()
@click.option('-v', '--verbose', count=True)
def log(verbose):
    click.echo('Verbosity: %s' % verbose)

# @cli.command()
# @click.option('/debug;/no-debug')
# def log(debug):
#     click.echo('debug=%s' % debug)

@cli.command()
@click.option('--shout/--no-shout', ' /-S', default=False)
def info(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)

@cli.command()
@click.option('--upper', 'transformation', flag_value='upper',
              default=True)
@click.option('--lower', 'transformation', flag_value='lower')
def feature_switches(transformation):
    click.echo(getattr(sys.platform, transformation)())

@cli.command()
# @click.option('--password', prompt=True, hide_input=True,
#               confirmation_prompt=True)
@click.password_option()
def encrypt(password):
    # click.echo('Encrypting password to %s' % password.encode('rot13'))
    click.echo('Encrypting password to %s' % codecs.encode(password, 'rot-13'))

@cli.command()
# @click.option('--username', prompt=True,
@click.option('--username', prompt=False if os.environ.get('USER', '') else True,
              default=lambda: os.environ.get('USER', ''),
              show_default='current user')
def read_user(username):
    print("Hello,", username)

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    # click.echo('Version 1.0')
    click.echo(version)
    ctx.exit()

@cli.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def callbacks_eager():
    click.echo('Hello World!')

# @click.group()
# @click.option('--debug/--no-debug')
# def cli(debug):
#     click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()
@click.option('--username', envvar=f'{APP.upper()}_USERNAME')
def greet(username):
    click.echo('Hello %s!' % username)

@cli.command()
# @click.option('paths', '--path', envvar='PATHS', multiple=True,
@click.option('paths', '--path', envvar='PATH', multiple=True,
              type=click.Path())
def perform(paths):
    for path in paths:
        click.echo(path)

@cli.command()
@click.option('+w/-w')
def chmod(w):
    click.echo('writable=%s' % w)

def validate_rolls(ctx, param, value):
    try:
        rolls, dice = map(int, value.split('d', 2))
        return (dice, rolls)
    except ValueError:
        raise click.BadParameter('rolls need to be in format NdM')

@cli.command()
@click.option('--rolls', callback=validate_rolls, default='1d6', show_default=True)
def roll(rolls):
    click.echo('Rolling a %d-sided dice %d time(s)' % rolls)

def main():
    cli(prog_name=APP)
    cli.add_command(initdb)
    cli.add_command(dropdb)
    cli.add_command(parse_str)
    cli.add_command(parse_int)
    cli.add_command(parse_float)
    cli.add_command(parse_bool)
    cli.add_command(parse_uuid)
    cli.add_command(inout)
    cli.add_command(touch)
    cli.add_command(digest)
    cli.add_command(repeat)
    cli.add_command(parse_datetime)
    cli.add_command(convert)
    cli.add_command(putitem)
    cli.add_command(commit)
    cli.add_command(log)
    cli.add_command(info)
    cli.add_command(feature_switches)
    cli.add_command(encrypt)
    cli.add_command(read_user)
    cli.add_command(callbacks_eager)
    cli.add_command(greet)
    cli.add_command(perform)
    cli.add_command(chmod)
    cli.add_command(roll)


if __name__ == '__main__':
    # do_hello() # pragma: no cover
    # hello() # pragma: no cover
    # cli() # pragma: no cover
    main() # pragma: no cover
