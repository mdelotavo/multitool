import configparser
import os
import shutil
import stat
import sys
import uuid
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
  mkdir,
  touch,
  for_each_file,
  is_dir,
  is_file,
  read_file,
)
from multitool.verbose import common_verbose_options

try:
    from git import Repo

    HAS_GIT = True
    HELP = "Manage plugin repositories."
except ImportError:
    HAS_GIT = False
    HELP = "Manage plugin repositories. Git is required."


def require_git():
    if not HAS_GIT:
        sys.exit(0)


def init():
    mkdir(MULTITOOL_PLUGINS_DIRECTORY)
    touch(MULTITOOL_PLUGINS_PATH)
    touch(MULTITOOL_PLUGINS_CONFIG_FILE)


def config(section="sources"):
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg.read(MULTITOOL_PLUGINS_CONFIG_FILE)
    return dict(cfg._sections.get(section, {}))


def clone():
    init()
    for name, uri in config().items():
        dest = Path(MULTITOOL_PLUGINS_DIRECTORY) / name
        if is_dir(dest):
            continue

        console.echo(f"Installing {name}... ", end="", flush=True)
        try:
            Repo.clone_from(uri, dest)
            console.echo("Done")
        except Exception as e:
            console.echo(e)


def update_repos():

    def fn(p):
        if not is_dir(p):
            return

        console.echo(f"Updating {Path(p).stem}... ", end="", flush=True)

        try:
            repo = Repo(p)
            if not repo.bare:
                repo.remotes["origin"].pull()
            console.echo("Done")
        except Exception as e:
            console.echo(e)

    for_each_file(MULTITOOL_PLUGINS_DIRECTORY, fn, glob="[!.][!__]*")


def _chmod(func, p, _):
    os.chmod(p, stat.S_IRWXU)
    func(p)


def prune_repos():
    sources = config()

    def fn(p):
        if not is_dir(p):
            return

        name = Path(p).stem

        if name in sources:
            return

        repo = Path(p) / ".git"

        if not repo.exists():
            console.echo(f"Skipping {name}: local plugin directory without Git metadata.")
            console.echo("Remove it manually if it is no longer required.")
            return

        console.echo(f"Removing {name}... ", end="", flush=True)

        try:
            try:
                shutil.rmtree(p, onexc=_chmod)
            except TypeError:
                shutil.rmtree(p, onerror=_chmod)

            console.echo("Done")
        except Exception as e:
            console.echo(e)

    for_each_file(MULTITOOL_PLUGINS_DIRECTORY, fn, glob="[!.][!__]*")


def plugin_info(name):
    f = Path(MULTITOOL_PLUGINS_DIRECTORY) / name / f"{APP}-info.json"

    if not is_file(f):
        return None

    return read_file(f, type="json")


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
        prune_repos()
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
def prune(silent, verbose):
    require_git()
    prune_repos()


@plugins.command()
@common_silent_options
@common_verbose_options
@click.argument("name")
def new(silent, verbose, name):
    init()

    if not name.isidentifier():
        console.echo(f'Invalid plugin name "{name}".')
        sys.exit(1)

    root = Path(MULTITOOL_PLUGINS_DIRECTORY) / name

    if root.exists():
        console.echo(f'Plugin "{name}" already exists.')
        sys.exit(1)

    module = f"plugin_{uuid.uuid4().hex}"

    mkdir(root)

    (root / "__init__.py").write_text(f"""plugins = []

from .{module} import {name}
plugins.append("{name}")

__all__ = plugins
""")

    (root / f"{module}.py").write_text(
      f'''import click


@click.group()
def {name}():
    """Example Click plugin template."""
    pass


@{name}.command()
@click.argument(
    "message",
)
@click.option(
    "--count",
    "-c",
    type=int,
    default=1,
    show_default=True,
    help="Number of times to print the message.",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "json"]),
    default="text",
    show_default=True,
    help="Output format.",
)
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Increase verbosity level.",
)
@click.option(
    "--enabled/--disabled",
    default=True,
    help="Enable or disable the operation.",
)
@click.option(
    "--tag",
    "-t",
    multiple=True,
    help="Specify multiple tags.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Optional output file.",
)
@click.argument(
    "input_file",
    required=False,
    type=click.File("r"),
)
def hello(
    message,
    count,
    output_format,
    verbose,
    enabled,
    tag,
    output,
    input_file,
):
    """Example command showing common Click arguments and options."""

    result = {{
        "message": message,
        "count": count,
        "format": output_format,
        "verbose": verbose,
        "enabled": enabled,
        "tags": tag,
        "output": output,
        "input": input_file.name if input_file else None,
    }}

    if output_format == "json":
        import json
        result = json.dumps(result, indent=2)

    else:
        result = str(result)

    if output:
        with open(output, "w") as f:
            f.write(result)
    else:
        click.echo(result)
'''
    )

    (root / "multitool-info.json").write_text("""{
  "Homepage": "",
  "Requires": "",
  "Maintainer": "",
  "Description-en": ""
}
""")

    touch(root / "README.md")
    touch(root / "LICENSE")

    console.echo(f'Created plugin "{name}" at:')
    console.echo(f"  {root}")
    console.echo()
    console.echo("Generated module:")
    console.echo(f"  {module}.py")
    console.echo()
    console.echo("Next steps:")
    console.echo("  • Add commands to:")
    console.echo(f"      {module}.py")
    console.echo()
    console.echo("  • To use this plugin locally:")
    console.echo("      Copy the plugin directory into another Multitool")
    console.echo("      plugins directory:")
    console.echo("        ~/.multitool/plugins/")
    console.echo()
    console.echo("  • To distribute this plugin:")
    console.echo("      1. Initialize a Git repository.")
    console.echo("      2. Commit and push it to a remote source")
    console.echo("         (GitHub, GitLab, or another Git server).")
    console.echo("      3. Add the repository URL to your plugin config:")
    console.echo(f"           {APP} plugins configure")
    console.echo()
    console.echo("         Example:")
    console.echo()
    console.echo("           [sources]")
    console.echo(f"           {name} = https://github.com/<user>/{name}.git")
    console.echo()
    console.echo("         HTTPS and SSH Git URLs are supported.")
    console.echo()
    console.echo("      4. Install or update plugins:")
    console.echo(f"           {APP} plugins update")
