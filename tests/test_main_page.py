#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    test_main_page.py
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
import time
import unittest

# Third-party imports -----------------------------------------------

# Our own imports ---------------------------------------------------
from pages.main_page import *
from pages.login_page import LogInPage
from utils.test_cases import test_cases
from tests.base_test import BaseTest, BASE_URL

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
class TestMainPage(BaseTest):

    def test_page_load(self):
        print("\n" + str(test_cases(0)))
        login_page = LogInPage(self.driver)
        login_page.login_with_valid_user("valid_user")
        main_page = MainPage(self.driver)
        time.sleep(5)
        self.assertTrue(main_page.check_page_loaded(BASE_URL + '/dashboard'))

    def test_click_les_notes_de_frais_button(self):
        print("\n" + str(test_cases(1)))
        login_page = LogInPage(self.driver)
        login_page.login_with_valid_user("valid_user")
        main_page = MainPage(self.driver)
        result = main_page.click_les_notes_de_frais_button()
        self.assertIn(BASE_URL + '/expenses', result.get_url())

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
