import configparser
import os
import shutil
import stat
import sys
from pathlib import Path

import click
from click_option_group import MutuallyExclusiveOptionGroup, optgroup

from multitool import (
  APP,
  MULTITOOL_PLUGINS_CONFIG_FILE,
  MULTITOOL_PLUGINS_DIRECTORY,
  MULTITOOL_PLUGINS_PATH,
  console,
)
from multitool.silent import common_silent_options
from multitool.utils import (
  create_directory,
  create_empty_file,
  execute_function_on_directory_files,
  is_directory,
  is_regular_file,
  read_file_content,
)
from multitool.verbose import common_verbose_options

try:
    from git import Repo

    HAS_GIT = True
    HELP = "Plugins manager for distributing commands."
except ImportError:
    HAS_GIT = False
    HELP = "Plugins manager. Git is required."


def require_git():
    if not HAS_GIT:
        sys.exit(0)


def init():
    create_directory(MULTITOOL_PLUGINS_DIRECTORY)
    create_empty_file(MULTITOOL_PLUGINS_PATH)
    create_empty_file(MULTITOOL_PLUGINS_CONFIG_FILE)


def config(section="sources"):
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg.read(MULTITOOL_PLUGINS_CONFIG_FILE)
    return dict(cfg._sections.get(section, {}))


def clone():
    init()
    for name, uri in config().items():
        dest = Path(MULTITOOL_PLUGINS_DIRECTORY) / name
        if is_directory(dest):
            continue

        console.echo(f"Installing {name}... ", line_ending="", should_flush=True)
        try:
            Repo.clone_from(uri, dest)
            console.echo("Done")
        except Exception as e:
            console.echo(e)


def update_repos():

    def fn(p):
        if not is_directory(p):
            return

        console.echo(f"Updating {Path(p).stem}... ", line_ending="", should_flush=True)

        try:
            repo = Repo(p)
            if not repo.bare:
                repo.remotes["origin"].pull()
            console.echo("Done")
        except Exception as e:
            console.echo(e)

    execute_function_on_directory_files(MULTITOOL_PLUGINS_DIRECTORY, fn, glob="[!.][!__]*")


def prune():
    sources = config()

    def fn(p):
        if not is_directory(p):
            return

        name = Path(p).stem
        if name in sources:
            return

        console.echo(f"Removing {name}... ", line_ending="", should_flush=True)

        try:
            shutil.rmtree(p, onerror=_chmod)
            console.echo("Done")
        except Exception as e:
            console.echo(e)

    execute_function_on_directory_files(MULTITOOL_PLUGINS_DIRECTORY, fn, glob="[!.][!__]*")


def _chmod(func, p, _):
    os.chmod(p, stat.S_IRWXU)
    func(p)


# def prune():
#     sources = config()

#     def fn(p):
#         if not is_directory(p):
#             return

#         name = Path(p).stem
#         if name in sources:
#             return

#         console.echo(f"Removing {name}... ", line_ending="", should_flush=True)

#         try:
#             shutil.rmtree(p, onexc=_chmod)
#             console.echo("Done")
#         except Exception as e:
#             console.echo(e)

#     execute_function_on_directory_files(PLUGINS_DIR, fn, glob="[!.][!__]*")

# def _chmod(func, path, exc):
#     os.chmod(path, stat.S_IRWXU)
#     func(path)


def plugin_info(name):
    f = Path(MULTITOOL_PLUGINS_DIRECTORY) / name / f"{APP}-info.json"

    if not is_regular_file(f):
        return None

    return read_file_content(f, type="json")


def print_commit(name):
    repo = Repo(Path(MULTITOOL_PLUGINS_DIRECTORY) / name)
    console.echo(repo.git.log("--pretty=format:%h - %s (%cr) <%an>", "-1"))


@click.group(help=HELP)
def plugins():
    pass


@plugins.command()
@common_silent_options
@common_verbose_options
@click.option("-a/-A", "--apply-changes/--no-apply-changes", default=False)
def configure(silent, verbose, apply_changes):
    require_git()
    init()

    click.edit(filename=MULTITOOL_PLUGINS_CONFIG_FILE)

    if apply_changes:
        clone()
        prune()
    else:
        console.echo(f"\nRun `{APP} plugins update` to apply changes.\n")


@plugins.command()
@common_silent_options
@common_verbose_options
def update(silent, verbose):
    require_git()
    clone()
    update_repos()


@plugins.command()
@common_silent_options
@common_verbose_options
@click.option("-n", "--name")
@optgroup.group("Filter options", cls=MutuallyExclusiveOptionGroup)
@optgroup.option("--show-commit-only/--no-show-commit-only", default=False)
@optgroup.option("--show-dependencies-only/--no-show-dependencies-only", default=False)
def show(silent, verbose, name, show_commit_only, show_dependencies_only):
    if not name:
        for k, v in config().items():
            console.echo(f"{k}: {v}")
        return

    info = plugin_info(name)
    if not info:
        return

    if show_commit_only:
        require_git()
        print_commit(name)
        return

    if show_dependencies_only:
        if info.get("Requires"):
            console.echo(info["Requires"])
        return

    for k, v in info.items():
        console.echo(f"{k}: {v}")


@plugins.command()
@common_silent_options
@common_verbose_options
def prune_cmd(silent, verbose):
    require_git()
    prune()
