import importlib
import inspect
import json
import logging
import os
import re
import sys
from pathlib import Path

import click


def gen_path_str(*args):
    if not args:
        return
    path = None
    for arg in args:
        if not path:
            path = Path(arg)
        else:
            path /= arg
    return str(path)


def is_dir(d):
    return os.path.isdir(d)


def is_envvar_true(value):
    return value in (True, 'True', 'true', '1')


def is_file(f):
    return os.path.isfile(f)


def import_all_modules_in_directory(plugins_init_file, existing_commands):
    try:
        spec = importlib.util.spec_from_file_location('plugins_modules', plugins_init_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        import plugins_modules
        from plugins_modules import __all__ as all_plugins_modules

        for module in all_plugins_modules:
            _module = getattr(plugins_modules, module)
            if isinstance(_module, (click.core.Command, click.core.Group)):
                existing_commands.add(_module)
    except ImportError:
        logging.warning(
            f'{inspect.stack()[0][3]}; will skip loading plugin: {module}', exc_info=True
        )


def make_dirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            logging.warning(f'{inspect.stack()[0][3]}; will ignore FileExistsError')


def read_file(file, type='text'):
    with open(file, 'r') as f:
        if type == 'json':
            return json.loads(f.read())
        return f.read()


def remove_file_above_size(file, size_kb=100):
    if os.path.getsize(file) > size_kb * 1024:
        os.remove(file)


def resolve_target_directory(target_directory=None):
    if target_directory:
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        return str(Path(target_directory).resolve())
    return os.getcwd()


def run_func_on_dir_files(dir, func, glob='**/*', args=(), kwargs={}):
    state = []
    for file_path in Path(resolve_target_directory(dir)).resolve().glob(glob):
        _tuple = (str(file_path),)
        result = func(*(_tuple + args), **kwargs)
        if result:
            state.append(result)
    return state


def run_func_on_iterable(iterable, func, state_op='append', args=(), kwargs={}):
    state = []
    for item in iterable:
        _tuple = (item,)
        result = func(*(_tuple + args), **kwargs)
        if result:
            getattr(state, state_op)(result)
    return state


def setup_global_logger(log_file):
    touch(log_file)
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    remove_file_above_size(log_file, size_kb=1000)


def show_message(msg):
    print(msg)


def touch(path):
    try:
        make_dirs(os.path.split(path)[0])
        if not os.path.exists(path):
            with open(path, 'x'):
                os.utime(path, None)
    except FileExistsError:
        logging.warning(f'{inspect.stack()[0][3]}; will ignore FileExistsError')
