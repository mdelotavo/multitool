from pathlib import Path

import click

from multitool import console
from multitool.silent import common_silent_options
from multitool.utils import mkdir, touch
from multitool.verbose import common_verbose_options

PROJECT_STRUCTURE = {
  "pyproject.toml": None,
  "{app}": {
    "__init__.py": None,
    "__main__.py": None,
    # "cls.py": None,
    "console.py": None,
    "exceptions.py": None,
    "silent.py": None,
    "utils.py": None,
    "utils_init.py": None,
    "verbose.py": None,
    "submodule": {
      "__init__.py": None,
      "commands.py": None,
    },
  },
}


def create_structure(root: Path, structure: dict, app: str):
    for name, children in structure.items():
        path = root / name.format(app=app)

        if children is None:
            touch(path)
        else:
            mkdir(path)
            create_structure(path, children, app)


@click.command(help="Create the directory structure for a new Python package project.")
@click.argument("name")
@click.argument(
  "directory",
  type=click.Path(path_type=Path),
  default=".",
  required=False,
)
@common_silent_options
@common_verbose_options
def bootstrap(silent, verbose, name, directory):
    root = directory / name
    mkdir(root)

    create_structure(root, PROJECT_STRUCTURE, name)

    console.echo(f"Created project: {root}")
