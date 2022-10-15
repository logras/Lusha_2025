#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    login_page.py
# @Directory   pages
# @Author      belr
# @Date        13/10/2022
"""
Log In page Class
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

# Our own imports ---------------------------------------------------
from utils import users
from utils.locators import *
from pages.base_page import BasePage
from pages.main_page import MainPage

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
class LogInPage(BasePage):
    def __init__(self, driver):
        self.locator = LoginPageLocators
        super().__init__(driver)  # Python3 version

    def enter_email(self, email):
        self.find_element(*self.locator.EMAIL).send_keys(email)

    def enter_password(self, password):
        self.find_element(*self.locator.PASSWORD).send_keys(password)

    def click_login_button(self):
        self.find_element(*self.locator.SUBMIT).click()

    def login(self, user):
        user = users.get_user(user)
        print(user)
        self.enter_email(user["email"])
        self.enter_password(user["password"])
        self.click_login_button()

    def login_with_valid_user(self, user):
        self.login(user)
        return MainPage(self.driver)

    def login_with_invalid_user(self, user):
        self.login(user)
        return self.find_element(*self.locator.ERROR_MESSAGE).text

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
