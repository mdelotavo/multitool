APP = 'multitool'
__version__ = '0.3.2'
description = 'General-purpose command-line interface with plugins support'
# long_description = 'General-purpose command-line interface with plugins support'

import builtins
from pathlib import Path

from multitool.utils import create_directory

MULTITOOL_TOGGLE_SILENT = False
MULTITOOL_TOGGLE_VERBOSE = 0

MULTITOOL_DIRECTORY = create_directory(Path.home(), '.multitool')

MULTITOOL_LOG_FILE = create_directory(MULTITOOL_DIRECTORY, f'{APP}.log')

MULTITOOL_PLUGINS_DIRECTORY = create_directory(MULTITOOL_DIRECTORY, 'plugins')
MULTITOOL_PLUGINS_CONFIG_FILE = create_directory(MULTITOOL_PLUGINS_DIRECTORY, 'config')
MULTITOOL_PLUGINS_PATH = create_directory(MULTITOOL_PLUGINS_DIRECTORY, '__init__.py')

builtins.MULTITOOL_TOGGLE_SILENT = MULTITOOL_TOGGLE_SILENT
builtins.MULTITOOL_TOGGLE_VERBOSE = MULTITOOL_TOGGLE_VERBOSE
