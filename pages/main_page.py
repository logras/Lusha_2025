#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    main_page.py
# @Directory   pages
# @Author      belr
# @Date        13/10/2022
"""
Main page Class
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
class MainPage(BasePage):
    def __init__(self, driver):
        self.locator = MainPageLocators
        super().__init__(driver)  # Python3 version

    def check_page_loaded(self, url):
        # return True if self.find_element(*self.locator.LOGO) else False
        return True if self.get_url() == url else False

    def click_les_notes_de_frais_button(self):
        self.find_element(*self.locator.NOTES_DE_FRAIS).click()
        self.find_element(*self.locator.LES_NOTES_DE_FRAIS).click()
        return LesNotesDeFraisPage(self.driver)

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
