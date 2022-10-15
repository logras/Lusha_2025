#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    test_login_page.py
# @Directory   tests
# @Author      belr
# @Date        13/10/2022
"""
unittest for asserting cases.
In this module, there should be test cases.
If you want to run it, you should type: python <module-name.py>
"""
# -----------------------------------------------------------------------------
# Copyright (c) 2015, the IPython Development Team and José Fonseca.
#
# Distributed under the terms of the Creative Commons License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#
#
# REFERENCES:
# http://ipython.org/ipython-doc/rel-0.13.2/development/coding_guide.html
# https://www.python.org/dev/peps/pep-0008/
# -----------------------------------------------------------------------------
'''
OPTIONS ------------------------------------------------------------------
A description of each option that can be passed to this script
ARGUMENTS -------------------------------------------------------------
A description of each argument that can or must be passed to this script
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

# stdlib imports -------------------------------------------------------
# import os
# import sys
import unittest

# Third-party imports -----------------------------------------------

# Our own imports ---------------------------------------------------
from tests.base_test import *
from pages.login_page import *
from tests.base_test import BaseTest
from utils.test_cases import test_cases

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# LOCAL UTILITIES
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------
class TestLogInPage(BaseTest):

    def test_login_with_valid_user(self):
        print("\n" + str(test_cases(4)))
        login_page = LogInPage(self.driver)
        result = login_page.login_with_valid_user("valid_user")
        self.assertIn(BASE_URL, result.get_url())

    def test_login_with_invalid_user(self):
        print("\n" + str(test_cases(5)))
        login_page = LogInPage(self.driver)
        result = login_page.login_with_invalid_user("invalid_user")
        self.assertIn("Ce compte n'existe pas", result)

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
