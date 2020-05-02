#!/usr/bin/env python

# test_sync.py

from click.testing import CliRunner
from multitool.__main__ import cli

def test_sync():
    runner = CliRunner()
    result = runner.invoke(cli, ['--debug', 'sync'])
    # result = runner.invoke(cli, ['--debug', 'sync'], terminal_width=60)
    assert result.exit_code == 0
    # assert 'Debug mode is on' in result.output
    assert 'Debug is on' in result.output
    assert 'Syncing' in result.output

test_sync()
