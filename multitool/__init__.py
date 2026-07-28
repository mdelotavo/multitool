APP = "multitool"
__version__ = "0.7.0"
description = "Create and run plugin-based command-line tools."
long_description = ("Create and run plugin-based command-line tools by dynamically loading Click commands from local or Git-managed plugin repositories.")

import builtins
from pathlib import Path

from multitool.utils_init import join_path

MULTITOOL_TOGGLE_SILENT = False
MULTITOOL_TOGGLE_VERBOSE = 0

MULTITOOL_DIRECTORY = join_path(Path.home(), ".multitool")

MULTITOOL_LOG_FILE = join_path(MULTITOOL_DIRECTORY, f"{APP}.log")

MULTITOOL_PLUGINS_DIRECTORY = join_path(MULTITOOL_DIRECTORY, "plugins")
MULTITOOL_PLUGINS_CONFIG_FILE = join_path(MULTITOOL_PLUGINS_DIRECTORY, "config")
MULTITOOL_PLUGINS_PATH = join_path(MULTITOOL_PLUGINS_DIRECTORY, "__init__.py")

builtins.MULTITOOL_TOGGLE_SILENT = MULTITOOL_TOGGLE_SILENT
builtins.MULTITOOL_TOGGLE_VERBOSE = MULTITOOL_TOGGLE_VERBOSE
