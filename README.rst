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

----------------
Managing plugins
----------------

The simple plugins manager uses Git to install commands from remote sources, thus you will need to have Git installed for installation to work.
However, it is possible to install plugins manually by storing plugins in the correct location (to be documented).

Currently, only the commands shown below are supported. More commands will be added to improve automation and user experience.

The steps below show how to install commands from a public plugins repository located here:

* https://github.com/mdelotavo/multitool-plugins

^^^^^^^^^^^
Configuring
^^^^^^^^^^^

To configure remote sources for installing plugins, run::

    multitool plugins configure -a

This will open a text editor so that you can specify the remote sources.

If you don't want changes to be automatically applied, then you can drop the ``-a`` option.

When the editor opens, copy and paste the following example configuration::

    [sources]
    public = https://github.com/mdelotavo/multitool-plugins.git

After saving the changes, the CLI will attempt to install the plugins from the specified Git URI.
Here we use the HTTPS URI but you can also use SSH if you have configured it.

You can also specify multiple sources, as long as the key (``public`` in this case) is unique.
The key will be the name of the repository on your local machine under ``~/.multitool/plugins/``.

If installation is successful, you should now see additional commands when you run ``multitool -h``

^^^^^^^^
Updating
^^^^^^^^

If you specified the ``-a`` option when running ``multitool plugins configure`` then install will occur automatically.
Otherwise you can run::

     multitool plugins update

This will install and update plugins.

^^^^^^^
Pruning
^^^^^^^

If you specified the ``-a`` option when running ``multitool plugins configure`` then the removal of plugins will occur automatically.
Otherwise you can run::

     multitool plugins prune

^^^^^^^
Showing
^^^^^^^

To show the plugins you have configured, run::

     multitool plugins show

You can also run the following commands if you specify the plugin name::

    multitool plugins show -n PLUGIN_NAME --show-commit-only
    multitool plugins show -n PLUGIN_NAME --show-dependencies-only

Some plugins will not load if dependencies are not installed. You can run the following command to install them.
In order for this to work, the plugin needs to have the ``Requires`` key in the JSON body of the ``multitool-info.json`` file.
More details coming soon.::

    pip3 install $(multitool plugins show -n PLUGIN_NAME --show-dependencies-only)

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
