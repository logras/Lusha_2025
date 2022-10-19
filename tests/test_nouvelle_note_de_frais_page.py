#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    test_nouvelle_note_de_frais_page.py
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
import pytest
import allure

# Our own imports ---------------------------------------------------
from tests.base_test import *
from utils.test_cases import formal_test_cases
from pages.login_page import LogInPage

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# LOCAL UTILITIES
# -----------------------------------------------------------------------------
purchase_supplier = 'BelR'
purchase_date = time.strftime("%d/%m/%Y")
purchase_amount = 1000000


# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------
@allure.testcase(BASE_URL + '/expenses', 'Nouvelle note de frais form')
@pytest.mark.usefixtures("db_class")
class TestNouvelleNoteDeFraisPage(BaseTest):

    @allure.step("Remplir formulaire in Nouvelle note de frais page")
    @allure.severity(formal_test_cases(3)[0])
    def test_remplir_formulaire(self):
        print("\n" + str(formal_test_cases(3)))
        login_page = LogInPage(self.driver)
        main_page = login_page.login_with_valid_user("valid_user")
        les_notes_de_frais_page = main_page.click_les_notes_de_frais_button()
        nouvelle_note_de_frais_page = les_notes_de_frais_page.click_nouvelle_note_button()
        result = nouvelle_note_de_frais_page.remplir_formulaire(purchase_supplier, purchase_date, purchase_amount)
        time.sleep(5)
        self.assertIn(BASE_URL + '/expenses', result.get_url(), "No matching URL")

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
