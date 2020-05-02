#!/usr/bin/env python

# test_cat.py

from click.testing import CliRunner
from multitool.__main__ import cli

def test_cat():
    runner = CliRunner()
    with runner.isolated_filesystem():
      with open('hello.txt', 'w') as f:
          f.write('Hello World!')

      result = runner.invoke(cli, ['cat', 'hello.txt'])
      assert result.exit_code == 0
      assert result.output == 'Hello World!\n'

test_cat()
