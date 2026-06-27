APP = 'multitool'
__version__ = "0.6.0"
description = 'Quickly create and distribute command-line tools.'
long_description = 'Quickly create and distribute command-line tools with plugins.'

import builtins
from pathlib import Path

from multitool.utils import join_path_components

MULTITOOL_TOGGLE_SILENT = False
MULTITOOL_TOGGLE_VERBOSE = 0

MULTITOOL_DIRECTORY = join_path_components(Path.home(), '.multitool')

MULTITOOL_LOG_FILE = join_path_components(MULTITOOL_DIRECTORY, f'{APP}.log')

MULTITOOL_PLUGINS_DIRECTORY = join_path_components(MULTITOOL_DIRECTORY, 'plugins')
MULTITOOL_PLUGINS_CONFIG_FILE = join_path_components(MULTITOOL_PLUGINS_DIRECTORY, 'config')
MULTITOOL_PLUGINS_PATH = join_path_components(MULTITOOL_PLUGINS_DIRECTORY, '__init__.py')

builtins.MULTITOOL_TOGGLE_SILENT = MULTITOOL_TOGGLE_SILENT
builtins.MULTITOOL_TOGGLE_VERBOSE = MULTITOOL_TOGGLE_VERBOSE
