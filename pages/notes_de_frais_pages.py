#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    notes_de_frais_pages.py
# @Directory   pages
# @Author      belr
# @Date        13/10/2022
"""
Notes de frais page Class
Page objects are written in this module.
Depends on the page functionality we can have more functions for new classes
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

# Third-party imports -----------------------------------------------
from selenium.webdriver.common.keys import Keys

# Our own imports ---------------------------------------------------
from utils.locators import *
from pages.base_page import BasePage

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
class LesNotesDeFraisPage(BasePage):
    def __init__(self, driver):
        self.locator = LesNotesDeFraisPageLocators
        super().__init__(driver)  # Python3 version

    def click_nouvelle_note_button(self):
        self.find_element(*self.locator.NOUVELLE_NOTE).click()
        return NouvelleNoteDeFraisPage(self.driver)


class NouvelleNoteDeFraisPage(BasePage):
    def __init__(self, driver):
        self.locator = NouvelleNoteDeFraisPageLocators
        super().__init__(driver)  # Python3 version

    def remplir_formulaire(self, supplier, date, amount):
        self.find_element(*self.locator.SUPPLIER).send_keys(supplier)
        self.find_element(*self.locator.SUPPLIER).send_keys(Keys.ENTER)
        self.find_element(*self.locator.DATE).send_keys(date)
        self.find_element(*self.locator.DATE).send_keys(Keys.ENTER)
        self.find_element(*self.locator.AMOUNT).send_keys(amount)
        self.find_element(*self.locator.AMOUNT).send_keys(Keys.ENTER)
        self.find_element(*self.locator.SUBMIT).click()

        return LesNotesDeFraisPage(self.driver)


# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
