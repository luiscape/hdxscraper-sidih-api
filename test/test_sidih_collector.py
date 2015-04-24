#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(dir, 'code'))

import mock
import unittest
import scraperwiki
from mock import patch
from sidih_collector import collect as Collect


class TestSidihCollector(unittest.TestCase):
  '''Unit tests for testing the collector script.'''

  def test_run_program(self):
    assert Collect.Main() == True
