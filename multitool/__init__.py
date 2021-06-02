APP = 'multitool'
__version__ = '0.2.1'
description = 'General-purpose command-line interface with plugins support'
# long_description = 'Multitool is general-purpose command-line interface with plugins support'

from os import getenv
from pathlib import Path

from multitool.utils import concat_str_path, is_true


MULTITOOL_TOGGLE_SILENT = False
MULTITOOL_TOGGLE_VERBOSE = 0

MULTITOOL_DIRECTORY = concat_str_path(Path.home(), '.multitool')

MULTITOOL_EXCEPTION_LOG_FILE = concat_str_path(MULTITOOL_DIRECTORY, 'exception.log')

MULTITOOL_PLUGINS_DIRECTORY = concat_str_path(MULTITOOL_DIRECTORY, 'plugins')
MULTITOOL_PLUGINS_CONFIG_FILE = concat_str_path(MULTITOOL_PLUGINS_DIRECTORY, 'config')
MULTITOOL_PLUGINS_PATH = concat_str_path(MULTITOOL_PLUGINS_DIRECTORY, '__init__.py')
