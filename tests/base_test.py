#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    base_test.py
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
# import sys
# import os
import unittest

# Third-party imports -----------------------------------------------
import pytest
# import xmlrunner
import HtmlTestRunner
from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Our own imports ---------------------------------------------------

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------
BASE_URL = config('KIWIHR_URL')

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# LOCAL UTILITIES
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------
# I am using python unittest for asserting cases.
# In this module, there should be test cases.
# If you want to run it, you should type: python <module-name.py>
@pytest.mark.usefixtures("db_class")
class BaseTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        # options.add_argument("--headless") # Runs Chrome in headless mode
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        # options.add_argument("--start-fullscreen")
        options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Firefox()

        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(BASE_URL)

    def tearDown(self):
        self.driver.quit()

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# RUNTIME PROCEDURE
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # suite = unittest.TestLoader().loadTestsFromTestCase(BaseTest)
    suite = unittest.defaultTestLoader.discover('.')
    # xmlrunner.XMLTestRunner().run(suite)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    HtmlTestRunner.HTMLTestRunner(combine_reports=True, output='reports').run(suite)
