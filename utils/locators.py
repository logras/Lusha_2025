#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    locators.py
# @Directory   utils
# @Author      belr
# @Date        13/10/2022
"""
For maintainability web objects locators are separated by page name Class
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
from selenium.webdriver.common.by import By

# Our own imports ---------------------------------------------------

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
class LoginPageLocators(object):
    EMAIL = (By.XPATH, '//*[@id="login"]')
    PASSWORD = (By.XPATH, '//*[@id="password"]')
    # SUBMIT = (By.XPATH, '//*[@id="app"]/div[1]/div/div/div/div/div/div/div/form/button')
    SUBMIT = (By.XPATH, '/html/body/div[1]/div[1]/div/div/div/div/div/div/div/form/button')
    # ERROR_MESSAGE = (By.ID, 'message_error')
    ERROR_MESSAGE = (By.XPATH, '//*[@id="app"]/div[1]/div/div/div/div/div/div/div/form/div[1]/div[1]/p')


class MainPageLocators(object):
    LOGO = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div/div[2]/a/svg')
    NOTES_DE_FRAIS = (By.XPATH, '//*[@id="app"]/div[1]/aside/ul/li[7]/div/span/span[2]')
    LES_NOTES_DE_FRAIS = (By.XPATH, '//*[@id="app"]/div[1]/aside/ul/li[7]/div/div/ul/li[1]/a')


class LesNotesDeFraisPageLocators(object):
    NOUVELLE_NOTE = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div[2]/article[1]/div/a')


class NouvelleNoteDeFraisPageLocators(object):
    SUPPLIER = (By.XPATH, '//*[@id="/expense/merchant"]')
    DATE = (By.XPATH, '//*[@id="/expense/purchaseDate"]')
    AMOUNT = (By.XPATH, '//*[@id="/expense/amount"]')
    SUBMIT = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div[2]/div/div/article/form/div[1]/div/div[1]/div/button')

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
