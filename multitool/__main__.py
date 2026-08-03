#!/usr/bin/env python
# __main__.py

import click

from multitool import APP, MULTITOOL_LOG_FILE, MULTITOOL_PLUGINS_DIRECTORY
from multitool import __version__ as version
from multitool.bootstrap.commands import bootstrap
from multitool.cls import AliasedGroup
from multitool.exceptions import wrap_with_exception_handling
from multitool.plugins.commands import plugins
from multitool.run.commands import run
from multitool.utils import configure_root_logger, for_each_file, load_plugins

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS, cls=AliasedGroup, invoke_without_command=False, chain=False)
@click.version_option(version, "-V", "--version")
@click.pass_context
def cli(ctx):
    """Create and run plugin-based command-line tools."""
    ctx.ensure_object(dict)


@wrap_with_exception_handling
def main():
    configure_root_logger(MULTITOOL_LOG_FILE)

    cli_commands = {plugins, run, bootstrap}

    run_commands = {}

    for_each_file(
      MULTITOOL_PLUGINS_DIRECTORY,
      load_plugins,
      args=(run_commands, ),
      glob="[!.][!__]*/__init__.py",
    )

    for command in run_commands.values():
        run.add_command(command)

    for command in cli_commands:
        cli.add_command(command)

    cli(prog_name=APP, obj={})


if __name__ == "__main__":
    main()
