#!/usr/bin/env python

# test_prompt.py

from click.testing import CliRunner
from multitool.__main__ import cli

def test_prompts():
    runner = CliRunner()
    result = runner.invoke(cli, ['prompt2'], input='wau wau\n')
    assert not result.exception
    assert result.output == 'Foo: wau wau\nfoo=wau wau\n'

test_prompts()
