multitool
=========
Multitool is a command-line interface template for learning how to package command-line tools using the Click package.

To learn more about Click, see the docs: https://click.palletsprojects.com/

To create a virtual environment:

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

-----
Usage
-----

.. code-block:: text

    Usage: multitool [OPTIONS] COMMAND [ARGS]...

      First paragraph.

      This is a very long second paragraph and as you can see wrapped very early
      in the source text but will be rewrapped to the terminal width in the
      final output.

      This is
      a paragraph
      without rewrapping.

      And this is a paragraph that will be rewrapped again.

    Options:
      -V, --version         Show the version and exit.
      --repo-home TEXT
      --debug / --no-debug
      -h, --help            Show this message and exit.

    Commands:
      ansi-colors
      callbacks-eager
      cat

    ...snip...

      sync
      touch               Print FILENAME if the file exists.
      write-file          Write 'Hello World!' to FILENAME.

-----------
``encrypt``
-----------
Non-interactive:

.. code-block:: text

    $ multitool encrypt --password asdf
    Encrypting password to nfqs

Interactive:

.. code-block:: text

    $ multitool encrypt
    Password:
    Repeat for confirmation:
    Encrypting password to nfqs
