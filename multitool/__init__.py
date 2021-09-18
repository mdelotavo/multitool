APP = 'multitool'
__version__ = '0.3.0'
description = 'General-purpose command-line interface with plugins support'
# long_description = 'General-purpose command-line interface with plugins support'

from pathlib import Path

from multitool.utils import generate_path_str

MULTITOOL_TOGGLE_SILENT = False
MULTITOOL_TOGGLE_VERBOSE = 0

MULTITOOL_DIRECTORY = generate_path_str(Path.home(), '.multitool')

MULTITOOL_LOG_FILE = generate_path_str(MULTITOOL_DIRECTORY, f'{APP}.log')

MULTITOOL_PLUGINS_DIRECTORY = generate_path_str(MULTITOOL_DIRECTORY, 'plugins')
MULTITOOL_PLUGINS_CONFIG_FILE = generate_path_str(MULTITOOL_PLUGINS_DIRECTORY, 'config')
MULTITOOL_PLUGINS_PATH = generate_path_str(MULTITOOL_PLUGINS_DIRECTORY, '__init__.py')
