#!/usr/bin/env python

# test_hello.py

from click.testing import CliRunner
from multitool.__main__ import hello

def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(hello, ['--count', '3', '--name', 'Peter'])
    assert result.exit_code == 0
    assert result.output == 'Hello, Peter!\nHello, Peter!\nHello, Peter!\n'

test_hello_world()
