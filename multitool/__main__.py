#!/usr/bin/env python
# __main__.py

import click

from multitool import APP, MULTITOOL_LOG_FILE, MULTITOOL_PLUGINS_DIRECTORY
from multitool import __version__ as version
from multitool.cls import AliasedGroup
from multitool.exceptions import wrap_with_exception_handling
from multitool.plugins.commands import plugins
from multitool.utils import (import_plugins_from_directory,
                             execute_function_on_directory_files, configure_global_logger)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    context_settings=CONTEXT_SETTINGS, cls=AliasedGroup, invoke_without_command=False, chain=False
)
@click.version_option(version, '-V', '--version')
@click.pass_context
def cli(ctx):
    """Welcome to the Multitool command-line interface!

    \b
    PyPI:   https://pypi.org/project/multitool/
    GitHub: https://github.com/mdelotavo/multitool

    \f

    :param click.core.Context ctx: Click context.
    """
    ctx.ensure_object(dict)


@wrap_with_exception_handling
def main():
    configure_global_logger(MULTITOOL_LOG_FILE)

    cli_commands = {plugins}

    execute_function_on_directory_files(
        MULTITOOL_PLUGINS_DIRECTORY,
        import_plugins_from_directory,
        args=(cli_commands,),
        glob='[!.][!__]*/__init__.py',
    )

    for command in cli_commands:
        cli.add_command(command)

    cli(prog_name=APP, obj={})


if __name__ == '__main__':
    main()  # pragma: no cover
