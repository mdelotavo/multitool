#!/usr/bin/env python

from unittest import TestCase
from unittest.mock import patch

from multitool.utils import show_message

class TestUtils(TestCase):

    @patch('builtins.print')
    def test_show_message(self, mock_print):
        text = 'this is a message'
        show_message(text)
        mock_print.assert_called_with(text)
