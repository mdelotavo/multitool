APP = "multitool"
__version__ = "0.9.0"
description = "Create and run plugin-based command-line tools."
long_description = ("Create and run plugin-based command-line tools by dynamically loading Click commands from local or Git-managed plugin repositories.")

import builtins
from pathlib import Path

from multitool.utils_init import join_path

# Runtime configuration
MULTITOOL_TOGGLE_SILENT = False
MULTITOOL_TOGGLE_VERBOSE = 0

# Application directories and files
MULTITOOL_DIRECTORY = join_path(Path.home(), ".multitool")
MULTITOOL_LOG_FILE = join_path(MULTITOOL_DIRECTORY, f"{APP}.log")

# Plugin directories and files
MULTITOOL_PLUGINS_DIRECTORY = join_path(MULTITOOL_DIRECTORY, "plugins")
MULTITOOL_PLUGINS_CONFIG_FILE = join_path(MULTITOOL_PLUGINS_DIRECTORY, "config")
MULTITOOL_PLUGINS_INIT_FILE = join_path(MULTITOOL_PLUGINS_DIRECTORY, "__init__.py")

# Expose runtime configuration globally
builtins.MULTITOOL_TOGGLE_SILENT = MULTITOOL_TOGGLE_SILENT
builtins.MULTITOOL_TOGGLE_VERBOSE = MULTITOOL_TOGGLE_VERBOSE
