#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    test_les_notes_de_frais_page.py
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
from tests.base_test import *
from utils.test_cases import test_cases
from pages.main_page import MainPage
from pages.login_page import LogInPage
from pages.notes_de_frais_pages import LesNotesDeFraisPage

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
class TestLesNotesDeFraisPage(BaseTest):

    def test_click_nouvelle_note_button(self):
        print("\n" + str(test_cases(2)))
        login_page = LogInPage(self.driver)
        login_page.login_with_valid_user("valid_user")
        main_page = MainPage(self.driver)
        main_page.click_les_notes_de_frais_button()
        result = LesNotesDeFraisPage(self.driver)
        result = result.click_nouvelle_note_button()
        time.sleep(5)
        self.assertIn(BASE_URL + '/expenses/new', result.get_url())

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
