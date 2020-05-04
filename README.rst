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

Usage:

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
      chmod
      clear
      clone
      commit
      convert
      copy                Move file SRC to DST.
      cp
      delete              delete the repo
      digest
      dropdb
      echo                Print value of SRC environment variable.
      edit                Edit FILENAME if the file exists.
      encrypt
      feature-switches
      get-commit-message
      get-streams
      getchar
      greet
      hello               Simple program that greets NAME for a total of COUNT...
      info
      init                init the repo
      initdb
      inout               Copy contents of INPUT to OUTPUT.
      launch              This can be used to open the default application...
      less
      log
      login
      parse-bool
      parse-datetime
      parse-float
      parse-int
      parse-str
      parse-uuid
      pause
      perform
      print-stdout
      progress-bar
      prompt
      prompt2
      putitem
      read-config         Print APP_NAME config file.
      read-user
      repeat
      repeat-float
      roll
      runserver
      sync
      touch               Print FILENAME if the file exists.
      write-file          Write 'Hello World!' to FILENAME.
