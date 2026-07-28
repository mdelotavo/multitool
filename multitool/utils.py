import importlib
import inspect
import json
import logging
import os
import sys
from pathlib import Path

import click


def configure_logger(log_file):
    touch(log_file)
    remove_if_large(log_file, size_kb=1000)
    logging.basicConfig(
      filename=log_file,
      level=logging.WARNING,
      format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def touch(path):
    try:
        mkdir(os.path.split(path)[0])
        if not os.path.exists(path):
            with open(path, "x"):
                os.utime(path, None)
    except FileExistsError:
        logging.warning(f"{inspect.stack()[0][3]}; will ignore FileExistsError")


def mkdir(path):
    if not path:
        return
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            logging.warning(f"{inspect.stack()[0][3]}; will ignore FileExistsError")


def for_each_file(dir, func, glob="**/*", args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    state = []
    for file_path in Path(resolve_dir(dir)).resolve().glob(glob):
        _tuple = (str(file_path), )
        result = func(*(_tuple + args), **kwargs)
        if result:
            state.append(result)
    return state


def resolve_dir(target_directory=None):
    if target_directory:
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        return str(Path(target_directory).resolve())
    return os.getcwd()


def load_plugins(init_file, commands):
    try:
        spec = importlib.util.spec_from_file_location(
          "plugins_modules",
          init_file,
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        plugins = getattr(module, "__all__", [])

        for name in plugins:
            obj = getattr(module, name)

            if not isinstance(obj, (click.Command, click.Group)):
                continue

            if name in commands:
                raise Exception(f'Duplicate plugin command "{name}" found in '
                                f"{init_file}. Already loaded from {commands[name].callback.__module__}")
            # if name in commands:
            #     raise RuntimeError(
            #       f'Plugin name conflict: "{name}". '
            #       f'Plugin command names must be unique across repositories. '
            #       f'Consider prefixing commands with the repository name.'
            #     )

            commands[name] = obj

    except ImportError:
        logging.warning("Failed to load plugin", exc_info=True)


def is_dir(d):
    return os.path.isdir(d)


def is_file(f):
    return os.path.isfile(f)


def read_file(file, type="text"):
    with open(file, "r") as f:
        return json.loads(f.read()) if type == "json" else f.read()


def remove_if_large(file, size_kb=100):
    if os.path.getsize(file) > size_kb * 1024:
        os.remove(file)


def show_message(msg):
    print(msg)
