multitool
=========

Multitool is a general-purpose command-line interface with plugins support.

--------------------
Why does this exist?
--------------------

I built this tool so I can quickly create and distribute command-line tools for consulting work and personal use.

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

The simple plugins manager uses ``git`` to install commands from remote sources, thus you will need to have ``git`` installed for the installation of plugins to work.

If ``git`` is unavailable on your machine, then the ``plugins`` commands will be unavailable.

However, it is possible to manually install plugins by dragging them under its own directory: ``~/.multitool/plugins/PLUGIN_NAME/``.

The tool revolves around the use of the `click`_ package to create command plugins which can be dynamically loaded into the ``multitool`` command-line at runtime.

Currently, only the commands shown below are supported. More commands will be added to improve automation and user experience.

The steps below show how to install commands from a `public plugins repository`_.

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

^^^^^^^^^^
Quickstart
^^^^^^^^^^

You can run the following commands to install the example plugins::

    echo -e '[sources]\npublic = https://github.com/mdelotavo/multitool-plugins.git' >> ~/.multitool/plugins/config
    multitool plugins update
    multitool plugins show
    multitool plugins show -n public
    multitool plugins show -n public --show-commit-only
    multitool plugins show -n public --show-dependencies-only
    pip3 install $(multitool plugins show -n public --show-dependencies-only)
    multitool examples -h

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

If you remove plugins from the config file or comment them out, and you then specified the ``-a`` option when running ``multitool plugins configure`` then the removal of plugins will occur automatically.
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
::

    pip3 install $(multitool plugins show -n PLUGIN_NAME --show-dependencies-only)

^^^^^^^^^^^^^^^
Troubleshooting
^^^^^^^^^^^^^^^

If you encounter issues with plugins or commands, you can find more detailed debug information and error messages in the log file:
::

    ~/.multitool/multitool.log

Reviewing this file can help you diagnose installation problems, missing dependencies, or Git-related errors.

.. ..
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

.. _`click`: https://click.palletsprojects.com/
.. _`multitool-plugins`: https://github.com/mdelotavo/multitool-plugins
.. _`public plugins repository`: https://github.com/mdelotavo/multitool-plugins
