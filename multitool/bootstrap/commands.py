from pathlib import Path

import click

from multitool import console
from multitool.silent import common_silent_options
from multitool.utils import mkdir
from multitool.verbose import common_verbose_options

PROJECT_STRUCTURE = {
  "pyproject.toml": None,
  "{app}": {
    "__init__.py": None,
    "__main__.py": None,
    "console.py": None,
    "exceptions.py": None,
    "request.py": None,
    "utils.py": None,
    "submodule": {
      "__init__.py": None,
      "commands.py": None,
    },
  },
}

FILE_TEMPLATES = {
  "pyproject.toml": """\
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "{app}"
version = "0.1.0"
description = "A Python package."
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "click>=8.1",
    "requests>=2.31",
]

[project.scripts]
{app} = "{app}.__main__:main"

[tool.setuptools.packages.find]
where = ["."]
""",
  "__init__.py": """\
\"\"\"{app} package.\"\"\"

__version__ = "0.1.0"
""",
  "__main__.py": """\
\"\"\"Command-line entry point for {app}.\"\"\"

from .submodule.commands import cli


def main() -> None:
    \"\"\"Run the command-line interface.\"\"\"
    cli()


if __name__ == "__main__":
    main()
""",
  "console.py": """\
\"\"\"Console output helpers.\"\"\"

import click


def echo(message: str = "") -> None:
    \"\"\"Print a normal message.\"\"\"
    click.echo(message)


def info(message: str) -> None:
    \"\"\"Print an informational message.\"\"\"
    click.echo(f"INFO: {message}")


def success(message: str) -> None:
    \"\"\"Print a success message.\"\"\"
    click.echo(f"OK: {message}")


def warning(message: str) -> None:
    \"\"\"Print a warning message.\"\"\"
    click.echo(f"WARNING: {message}")


def error(message: str) -> None:
    \"\"\"Print an error message to stderr.\"\"\"
    click.echo(f"ERROR: {message}", err=True)
""",
  "exceptions.py": """\
\"\"\"Application-specific exceptions.\"\"\"


class AppError(Exception):
    \"\"\"Base exception for application errors.\"\"\"


class ConfigurationError(AppError):
    \"\"\"Raised when configuration is invalid.\"\"\"


class ValidationError(AppError):
    \"\"\"Raised when input validation fails.\"\"\"


class RequestError(AppError):
    \"\"\"Raised when an HTTP request fails.\"\"\"

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response=None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response = response
""",
  "request.py": """\
\"\"\"Generic helpers for making REST API requests.\"\"\"

from typing import Any

import requests

from .exceptions import RequestError


DEFAULT_TIMEOUT = 30
DEFAULT_VERIFY_SSL = True


def request(
    method: str,
    url: str,
    *,
    params: dict[str, Any] | None = None,
    data: Any = None,
    json: Any = None,
    headers: dict[str, str] | None = None,
    timeout: int | float = DEFAULT_TIMEOUT,
    verify_ssl: bool = DEFAULT_VERIFY_SSL,
    **kwargs: Any,
) -> requests.Response:
    \"\"\"Make an HTTP request.\"\"\"
    try:
        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout,
            verify=verify_ssl,
            **kwargs,
        )

        response.raise_for_status()

        return response

    except requests.RequestException as exc:
        status_code = None

        if exc.response is not None:
            status_code = exc.response.status_code

        raise RequestError(
            str(exc),
            status_code=status_code,
            response=exc.response,
        ) from exc


def get(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int | float = DEFAULT_TIMEOUT,
    verify_ssl: bool = DEFAULT_VERIFY_SSL,
    **kwargs: Any,
) -> requests.Response:
    \"\"\"Make a GET request.\"\"\"
    return request(
        "GET",
        url,
        params=params,
        headers=headers,
        timeout=timeout,
        verify_ssl=verify_ssl,
        **kwargs,
    )


def post(
    url: str,
    *,
    data: Any = None,
    json: Any = None,
    headers: dict[str, str] | None = None,
    timeout: int | float = DEFAULT_TIMEOUT,
    verify_ssl: bool = DEFAULT_VERIFY_SSL,
    **kwargs: Any,
) -> requests.Response:
    \"\"\"Make a POST request.\"\"\"
    return request(
        "POST",
        url,
        data=data,
        json=json,
        headers=headers,
        timeout=timeout,
        verify_ssl=verify_ssl,
        **kwargs,
    )


def put(
    url: str,
    *,
    data: Any = None,
    json: Any = None,
    headers: dict[str, str] | None = None,
    timeout: int | float = DEFAULT_TIMEOUT,
    verify_ssl: bool = DEFAULT_VERIFY_SSL,
    **kwargs: Any,
) -> requests.Response:
    \"\"\"Make a PUT request.\"\"\"
    return request(
        "PUT",
        url,
        data=data,
        json=json,
        headers=headers,
        timeout=timeout,
        verify_ssl=verify_ssl,
        **kwargs,
    )


def patch(
    url: str,
    *,
    data: Any = None,
    json: Any = None,
    headers: dict[str, str] | None = None,
    timeout: int | float = DEFAULT_TIMEOUT,
    verify_ssl: bool = DEFAULT_VERIFY_SSL,
    **kwargs: Any,
) -> requests.Response:
    \"\"\"Make a PATCH request.\"\"\"
    return request(
        "PATCH",
        url,
        data=data,
        json=json,
        headers=headers,
        timeout=timeout,
        verify_ssl=verify_ssl,
        **kwargs,
    )


def delete(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    timeout: int | float = DEFAULT_TIMEOUT,
    verify_ssl: bool = DEFAULT_VERIFY_SSL,
    **kwargs: Any,
) -> requests.Response:
    \"\"\"Make a DELETE request.\"\"\"
    return request(
        "DELETE",
        url,
        headers=headers,
        timeout=timeout,
        verify_ssl=verify_ssl,
        **kwargs,
    )


def get_json(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int | float = DEFAULT_TIMEOUT,
    verify_ssl: bool = DEFAULT_VERIFY_SSL,
    **kwargs: Any,
) -> Any:
    \"\"\"Make a GET request and return decoded JSON.\"\"\"
    response = get(
        url,
        params=params,
        headers=headers,
        timeout=timeout,
        verify_ssl=verify_ssl,
        **kwargs,
    )

    try:
        return response.json()
    except ValueError as exc:
        raise RequestError(
            "Response did not contain valid JSON.",
            status_code=response.status_code,
            response=response,
        ) from exc
""",
  "utils.py": """\
\"\"\"General-purpose utility functions.\"\"\"

from pathlib import Path
from typing import Iterable


def ensure_directory(path: Path) -> Path:
    \"\"\"Create a directory if it does not already exist.\"\"\"
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_text(path: Path, encoding: str = "utf-8") -> str:
    \"\"\"Read text from a file.\"\"\"
    return path.read_text(encoding=encoding)


def write_text(
    path: Path,
    content: str,
    encoding: str = "utf-8",
) -> Path:
    \"\"\"Write text to a file, creating parent directories when needed.\"\"\"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)
    return path


def chunks(items: Iterable, size: int):
    \"\"\"Yield an iterable in chunks of the requested size.\"\"\"
    if size <= 0:
        raise ValueError("size must be greater than zero")

    chunk = []

    for item in items:
        chunk.append(item)

        if len(chunk) == size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
""",
  "submodule/__init__.py": """\
\"\"\"Submodule package for {app}.\"\"\"
""",
  "commands.py": """\
\"\"\"CLI commands for {app}.\"\"\"

import click

from .. import __version__
from ..exceptions import RequestError
from ..request import get_json, post


@click.group()
@click.version_option(__version__, prog_name="{app}")
def cli() -> None:
    \"\"\"Command-line interface for {app}.\"\"\"


@cli.command()
def hello() -> None:
    \"\"\"Run a simple example command.\"\"\"
    click.echo("Hello from {app}!")


@cli.command()
@click.argument("name")
def greet(name: str) -> None:
    \"\"\"Greet NAME.\"\"\"
    click.echo(f"Hello, {name}!")


@cli.command()
@click.option(
    "--insecure",
    is_flag=True,
    help="Disable SSL certificate verification.",
)
def api_get(insecure: bool) -> None:
    \"\"\"Example GET request against a REST API.\"\"\"
    try:
        data = get_json(
            "https://jsonplaceholder.typicode.com/todos/1",
            verify_ssl=not insecure,
        )

        click.echo(data)

    except RequestError as exc:
        raise click.ClickException(str(exc)) from exc


@cli.command()
@click.option(
    "--insecure",
    is_flag=True,
    help="Disable SSL certificate verification.",
)
def api_post(insecure: bool) -> None:
    \"\"\"Example POST request against a REST API.\"\"\"

    payload = {
        "title": "Example",
        "body": "Created by {app}.",
        "userId": 1,
    }

    try:
        response = post(
            "https://jsonplaceholder.typicode.com/posts",
            json=payload,
            verify_ssl=not insecure,
        )

        click.echo(response.json())

    except RequestError as exc:
        raise click.ClickException(str(exc)) from exc


@cli.command()
def rest_examples() -> None:
    \"\"\"Show REST API usage examples.\"\"\"

    click.echo(
        \"\"\"
REST API examples
=================

GET
---

from {app}.request import get

response = get(
    "https://jsonplaceholder.typicode.com/todos/1"
)

print(response.json())


GET JSON
--------

from {app}.request import get_json

todo = get_json(
    "https://jsonplaceholder.typicode.com/todos/1"
)

print(todo)


GET with query parameters
-------------------------

from {app}.request import get_json

users = get_json(
    "https://jsonplaceholder.typicode.com/users",
    params={{"id": 1}},
)

print(users)


POST
----

from {app}.request import post

response = post(
    "https://jsonplaceholder.typicode.com/posts",
    json={{
        "title": "Example",
        "body": "Hello from {app}",
        "userId": 1,
    }},
)

print(response.json())


PUT
---

from {app}.request import put

response = put(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={{
        "id": 1,
        "title": "Updated title",
        "body": "Updated body",
        "userId": 1,
    }},
)

print(response.json())


PATCH
------

from {app}.request import patch

response = patch(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={{
        "title": "Updated title",
    }},
)

print(response.json())


DELETE
------

from {app}.request import delete

response = delete(
    "https://jsonplaceholder.typicode.com/posts/1"
)

print(response.status_code)


SSL verification
----------------

SSL verification is enabled by default:

response = get(
    "https://api.example.com",
    verify_ssl=True,
)

To disable SSL verification:

response = get(
    "https://localhost:8443",
    verify_ssl=False,
)


CLI commands
------------

{app} --help
{app} hello
{app} greet Matthew
{app} api-get
{app} api-get --insecure
{app} api-post
{app} api-post --insecure
{app} rest-examples
\"\"\"
    )
""",
}


def create_structure(
  root: Path,
  structure: dict,
  app: str,
) -> None:
    """Create the project structure and populate files from templates."""

    for name, children in structure.items():
        path = root / name.replace("{app}", app)

        if children is None:
            content = FILE_TEMPLATES.get(name)

            if content is None:
                path.touch()
            else:
                path.parent.mkdir(parents=True, exist_ok=True)

                # Only replace our application-name placeholder.
                # Do not use str.format(), because generated Python
                # contains its own braces.
                content = content.replace("{app}", app)

                path.write_text(
                  content,
                  encoding="utf-8",
                )

        else:
            mkdir(path)

            create_structure(
              path,
              children,
              app,
            )


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

    create_structure(
      root,
      PROJECT_STRUCTURE,
      name,
    )

    console.echo(f"Created project: {root}")
