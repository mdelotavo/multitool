multitool
=========

Create and run plugin-based command-line tools.

----------
Quickstart
----------

This section shows how to start prototyping plugins on your local machine.
See the sections below to learn how to distribute your commands as remote
plugins that can be installed and updated from Git repositories.

Create a new local plugin::

    multitool plugins new test

Show the generated command help::

    multitool run test hello --help

Run the example command::

    multitool run test hello \
        "Hello, World!" \
        --count 3 \
        --format json \
        -vv \
        --enabled \
        --tag alpha \
        --tag beta \
        --output result.json

Edit the generated source code::

    vim ~/.multitool/plugins/test/plugin_*.py

-----
Usage
-----

.. code-block:: text

    Usage: multitool [OPTIONS] COMMAND [ARGS]...

      Create and run plugin-based command-line tools.

    Options:
      -V, --version  Show the version and exit.
      -h, --help     Show this message and exit.

    Commands:
      plugins  Manage plugin repositories.
      run      Run installed plugin commands.

----------------
Managing plugins
----------------

Plugins are distributed as Git repositories containing Click commands.

The ``plugins`` command manages plugin repositories, while installed plugin
commands are available under ``multitool run``.

Git is required to install or update plugins. If Git is unavailable, the
``plugins`` command cannot install repositories, although plugins can still be
installed manually by copying them into::

    ~/.multitool/plugins/PLUGIN_NAME/

^^^^^^^^^^^^^^^^
Creating plugins
^^^^^^^^^^^^^^^^

Create a new plugin scaffold with::

    multitool plugins new PLUGIN_NAME

This creates a local plugin repository under::

    ~/.multitool/plugins/PLUGIN_NAME/

The generated structure includes::

    PLUGIN_NAME/
    ├── __init__.py
    ├── plugin_<unique-id>.py
    ├── multitool-info.json
    ├── README.md
    └── LICENSE

The generated plugin contains a Click command group named
``PLUGIN_NAME`` and an example ``hello`` command. Add additional commands
to the generated ``plugin_<unique-id>.py`` module.

Test the plugin locally with::

    multitool run PLUGIN_NAME -h

To distribute the plugin:

1. Initialize the plugin directory as a Git repository::

       cd ~/.multitool/plugins/PLUGIN_NAME
       git init

2. Commit and push it to a remote Git repository such as GitHub or GitLab.

3. Add the repository URL to the Multitool configuration::

       [sources]
       PLUGIN_NAME = https://github.com/<user>/PLUGIN_NAME.git

4. Install or update plugins::

       multitool plugins update

Alternatively, copy the plugin directory directly into another Multitool
plugins directory to use it locally.

^^^^^^^^^^^
Configuring
^^^^^^^^^^^

Configure plugin repositories with::

    multitool plugins configure -a

This opens your editor to modify the plugin configuration. Omit ``-a`` if you
don't want changes applied automatically.

Example configuration::

    [sources]
    mdelotavo-multitool-plugins = https://github.com/mdelotavo/multitool-plugins.git

After saving, Multitool clones each configured repository into::

    ~/.multitool/plugins/

You can configure multiple repositories as long as each key is unique.

^^^^^^^^^^
Installing
^^^^^^^^^^

Install the example plugins::

    echo -e '[sources]\nmdelotavo-multitool-plugins = https://github.com/mdelotavo/multitool-plugins.git' >> ~/.multitool/plugins/config

    multitool plugins update
    multitool plugins show
    multitool plugins show -n mdelotavo-multitool-plugins
    multitool plugins show -n mdelotavo-multitool-plugins --show-commit-only
    multitool plugins show -n mdelotavo-multitool-plugins --show-dependencies-only
    pip3 install $(multitool plugins show -n mdelotavo-multitool-plugins --show-dependencies-only)

    multitool run examples -h

^^^^^^^^
Updating
^^^^^^^^

Install new plugins and update existing ones::

    multitool plugins update

^^^^^^^
Pruning
^^^^^^^

Remove repositories no longer listed in the configuration::

    multitool plugins prune

^^^^^^^
Showing
^^^^^^^

Show configured repositories::

    multitool plugins show

Or inspect a specific repository::

    multitool plugins show -n PLUGIN_NAME --show-commit-only
    multitool plugins show -n PLUGIN_NAME --show-dependencies-only

If a plugin declares Python dependencies in ``multitool-info.json``, install
them with::

    pip3 install $(multitool plugins show -n PLUGIN_NAME --show-dependencies-only)

---------------
Troubleshooting
---------------

If a plugin fails to install or load, check the log file::

    ~/.multitool/multitool.log

It contains installation, dependency, and Git-related errors.

-----------
Limitations
-----------

Plugin command names must be unique across all installed repositories.

To avoid naming conflicts, plugin modules should follow the convention of
including the repository owner and repository name in the command name.

For example, a repository configured as::

    [sources]
    mdelotavo-multitool-plugins = https://github.com/mdelotavo/multitool-plugins.git

should expose commands using a unique name such as::

    mdelotavo-multitool-plugins

This reduces the likelihood of collisions when multiple repositories expose
plugins with the same command name.

If duplicate command names are detected, Multitool will display an error
prompting you to delete the detected conflicting plugin repositories and, if
applicable, remove the corresponding remote sources from your plugin
configuration.


.. _`click`: https://click.palletsprojects.com/
.. _`multitool-plugins`: https://github.com/mdelotavo/multitool-plugins
.. _`public plugins repository`: https://github.com/mdelotavo/multitool-plugins
