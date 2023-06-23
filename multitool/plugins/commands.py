import configparser
import os
import shutil
import stat
import sys
from os import path
from pathlib import Path

import click
from click_option_group import MutuallyExclusiveOptionGroup, optgroup

from multitool import (MULTITOOL_PLUGINS_CONFIG_FILE,
                       MULTITOOL_PLUGINS_DIRECTORY, MULTITOOL_PLUGINS_PATH,
                       console)
from multitool.silent import common_silent_options
from multitool.utils import (is_directory, is_regular_file, create_directory, read_file_content,
                             execute_function_on_directory_files, create_empty_file)
from multitool.verbose import common_verbose_options

is_git_installed = False
plugins_command_help = 'Simple plugins manager for distributing commands.'

try:
    from git import Repo

    is_git_installed = True
except ImportError:
    plugins_command_help = '[Git not found! Please install Git first.] Simple plugins manager for distributing commands. This command requires Git to be installed.'


def chmod_directory(directory, mode):
    """
    Recursively changes the permissions of a directory and its contents.

    Reference: https://stackoverflow.com/a/58878271
    
    Args:
        directory (str): Path to the directory.
        mode (int): Permissions to be set (e.g., 0o0700).

    """
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            os.chmod(path.join(root, dir), mode)
        for file in files:
            os.chmod(path.join(root, file), mode)


def clone_plugin_repositories(section="sources"):
    initialize_MULTITOOL_plugins()
    config = load_plugin_config()
    if not config._sections:
        return
    sources = dict(config._sections[section])
    for name, uri in sources.items():
        dest = Path(MULTITOOL_PLUGINS_DIRECTORY) / name
        if is_directory(dest):
            continue
        try:
            console.echo(f"Installing {name}... ", line_ending="", should_flush=True)
            Repo.clone_from(uri, dest)
            console.echo("Done")
        except Exception as e:
            console.echo(e)


def exit_quietly_if_git_not_installed():
    if not is_git_installed:
        sys.exit(0)


def initialize_and_save_plugin_config():
    initialize_MULTITOOL_plugins()
    config = load_plugin_config()
    if not config._sections:
        return


def initialize_MULTITOOL_plugins():
    create_directory(MULTITOOL_PLUGINS_DIRECTORY)
    create_empty_file(MULTITOOL_PLUGINS_PATH)
    create_empty_file(MULTITOOL_PLUGINS_CONFIG_FILE)


def load_plugin_config(config_file=MULTITOOL_PLUGINS_CONFIG_FILE):
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(config_file)
    return config


def prune_unused_plugin_directories(section="sources"):
    initialize_MULTITOOL_plugins()
    config = load_plugin_config()
    if not config._sections:
        return
    sources = dict(config._sections[section])

    def _func(path):
        if not is_directory(path):
            return
        name = Path(path).stem
        if name in sources:
            return
        console.echo(f"Removing {name}... ", line_ending="", should_flush=True)
        plugin_directory = Path(MULTITOOL_PLUGINS_DIRECTORY) / name
        try:
            chmod_directory(str(Path(plugin_directory) / ".git"), stat.S_IRWXU)
            shutil.rmtree(plugin_directory)
            console.echo("Done")
        except Exception as e:
            console.echo(e)

    return execute_function_on_directory_files(MULTITOOL_PLUGINS_DIRECTORY, _func, glob="[!.][!__]*")


def update_plugin_repositories():
    def _func(path):
        if not is_directory(path):
            return
        console.echo(f"Updating {Path(path).stem}... ", line_ending="", should_flush=True)
        repo = Repo(path)
        if repo.bare:
            return
        try:
            repo.remotes["origin"].pull()
            console.echo("Done")
        except Exception as e:
            console.echo(e)

    return execute_function_on_directory_files(MULTITOOL_PLUGINS_DIRECTORY, _func, glob="[!.][!__]*")


@click.group(help=plugins_command_help)
def plugins():
    pass


@plugins.command(help="Edit config file manually.")
@common_silent_options
@common_verbose_options
@click.option(
    "-a/-A",
    "--apply-changes/--no-apply-changes",
    default=False,
    help="Install plugins from new sources after exiting the editor.",
    show_default=True,
)
def configure(silent, verbose, apply_changes):
    exit_quietly_if_git_not_installed()
    initialize_MULTITOOL_plugins()
    click.edit(filename=MULTITOOL_PLUGINS_CONFIG_FILE)
    if apply_changes:
        clone_plugin_repositories()
        prune_unused_plugin_directories()
    else:
        console.echo("\n  Run `apigee plugins update` to apply any changes,")
        console.echo("    or rerun `apigee plugins configure` with `-a`")
        console.echo("    to apply changes automatically.\n")


@plugins.command(help="Update or install plugins.")
@common_silent_options
@common_verbose_options
def update(silent, verbose, section="sources"):
    exit_quietly_if_git_not_installed()
    clone_plugin_repositories()
    update_plugin_repositories()


@plugins.command(help="Show plugins information.")
@common_silent_options
@common_verbose_options
@click.option("-n", "--name", help="name of the plugins package")
@optgroup.group(
    "Filter options", cls=MutuallyExclusiveOptionGroup, help="The filter options"
)
@optgroup.option(
    "--show-commit-only/--no-show-commit-only",
    default=False,
    help="only print latest Git commit log",
)
@optgroup.option(
    "--show-dependencies-only/--no-show-dependencies-only",
    default=False,
    help="only print list of required packages",
)
def show(
    silent,
    verbose,
    name,
    section="sources",
    show_commit_only=False,
    show_dependencies_only=False,
):
    if not name:
        config = load_plugin_config()
        if not config._sections:
            return
        sources = dict(config._sections[section])
        for name, uri in sources.items():
            console.echo(f"{name}: {uri}")
        return
    plugins_info_file = Path(MULTITOOL_PLUGINS_DIRECTORY) / name / "apigee-cli.info"
    if not is_regular_file(plugins_info_file):
        return
    plugins_info = read_file_content(plugins_info_file, type="json")
    if show_commit_only:
        exit_quietly_if_git_not_installed()
        console.echo(
            Repo(Path(MULTITOOL_PLUGINS_DIRECTORY) / name).git.log(
                "--pretty=format:%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset",
                "-1",
            )
        )
        return
    if show_dependencies_only:
        if plugins_info.get("Requires"):
            console.echo(plugins_info.get("Requires"))
        return
    for k, v in plugins_info.items():
        console.echo(f"{k}: {v}")


@plugins.command(help="Prune plugins with removed sources.")
@common_silent_options
@common_verbose_options
def prune(silent, verbose, section="sources"):
    exit_quietly_if_git_not_installed()
    prune_unused_plugin_directories()
