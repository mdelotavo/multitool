import importlib
import inspect
import json
import logging
import os
import re
import sys
from pathlib import Path

import click


def apply_function_on_iterable(iterable, func, state_op="append", args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    state = []
    for item in iterable:
        _tuple = (item,)
        result = func(*(_tuple + args), **kwargs)
        if result:
            getattr(state, state_op)(result)
    return state


def configure_global_logger(log_file):
    create_empty_file(log_file)
    remove_file_if_above_size(log_file, size_kb=1000)
    logging.basicConfig(
        filename=log_file,
        level=logging.WARNING,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def create_empty_file(path):
    try:
        create_directory(os.path.split(path)[0])
        if not os.path.exists(path):
            with open(path, "x"):
                os.utime(path, None)
    except FileExistsError:
        logging.warning(f"{inspect.stack()[0][3]}; will ignore FileExistsError")


def create_directory(path):
    if not path:
        return
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            logging.warning(f"{inspect.stack()[0][3]}; will ignore FileExistsError")


def execute_function_on_directory_files(dir, func, glob="**/*", args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    state = []
    for file_path in Path(get_resolved_directory_path(dir)).resolve().glob(glob):
        _tuple = (str(file_path),)
        result = func(*(_tuple + args), **kwargs)
        if result:
            state.append(result)
    return state


def get_resolved_directory_path(target_directory=None):
    if target_directory:
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        return str(Path(target_directory).resolve())
    return os.getcwd()


def import_plugins_from_directory(plugins_init_file, existing_commands):
    try:
        spec = importlib.util.spec_from_file_location('plugins_modules', plugins_init_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        import plugins_modules # type: ignore
        from plugins_modules import __all__ as all_plugins_modules # type: ignore

        for module in all_plugins_modules:
            _module = getattr(plugins_modules, module)
            if isinstance(_module, (click.core.Command, click.core.Group)):
                existing_commands.add(_module)
    except ImportError:
        logging.warning(
            f'{inspect.stack()[0][3]}; will skip loading plugin: {module}', exc_info=True
        )


def is_directory(d):
    return os.path.isdir(d)


def is_regular_file(f):
    return os.path.isfile(f)


def is_truthy_envvar(value):
    return value in (True, "True", "true", "1")


def join_path_components(*components):
    if not components:
        return
    path = None
    for component in components:
        if not path:
            path = Path(component)
        else:
            path /= component
    return str(path)


def read_file_content(file, type="text"):
    with open(file, "r") as f:
        return json.loads(f.read()) if type == "json" else f.read()


def remove_file_if_above_size(file, size_kb=100):
    if os.path.getsize(file) > size_kb * 1024:
        os.remove(file)


def show_message(msg):
    print(msg)
