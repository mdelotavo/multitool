multitool
=========
Multitool is general-purpose command-line interface with plugins support.

Multitool revolves around the use of the `click.palletsprojects`_ package for creating command plugins which are dynamically loadable into the command-line at runtime.

The plugins features are based off those found in the `apigeecli`_.

The plugins manager uses Git to manage plugins that can be installed from remote Git repositories. If Git is unavailable, then the plugins commands will not be available. However, it is possible to manually install plugins by dragging them into the correct locations.

Example plugins are available for installation here: `multitool-plugins`_.

------------
How it works
------------

1. The plugins manager ``multitool/plugins/commands.py`` will clone or pull remote repositories into ``~/.multitool/plugins/``.
2. The ``_load_all_modules_in_directory()`` function in ``multitool/__main__.py`` will attempt to import the functions as specified in the ``__init__.py`` file for each plugin repository found in ``~/.multitool/plugins/``.
3. If the functions found are of instance type ``(click.core.Command, click.core.Group)`` then the CLI will add it to the list of available commands.

Further details are to be documented, including how to write plugins and leverage some useful CLI libraries.

-----
Usage
-----

.. code-block:: text

    Usage: multitool [OPTIONS] COMMAND [ARGS]...

      Welcome to the Multitool command-line interface!

      PyPI:   https://pypi.org/project/multitool/
      GitHub: https://github.com/mdelotavo/multitool

    Options:
      -V, --version  Show the version and exit.
      -h, --help     Show this message and exit.

    Commands:
      plugins  Simple plugins manager for distributing commands.

----------------------------
Create a virtual environment
----------------------------

.. code-block:: text

    pip3 install virtualenv
    virtualenv venv
    source venv/bin/activate

    pip3 install -e .
    python3 -m multitool -V
    python3 -m multitool -h   # or just `multitool -h`

    pip3 install -r requirements.txt
    ./runtests.sh

    deactivate

.. _`click.palletsprojects`: https://click.palletsprojects.com/
.. _`apigeecli`: https://pypi.org/project/apigeecli/
.. _`multitool-plugins`: https://github.com/mdelotavo/multitool-plugins
