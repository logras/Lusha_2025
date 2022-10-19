#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium-page-objects-model-with-unittest
# @Filename    conftest.py
# @Directory   tests
# @Author      belr
# @Date        16/10/2022
"""
We define a fixture function below and it will be "used" by
referencing its name from tests
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

from os import path
from typing import Any, Callable, Optional

# Third-party imports -----------------------------------------------
import pytest

from pytest import fixture
from _pytest.fixtures import SubRequest

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Our own imports ---------------------------------------------------
from tests.base_test import BROWSER, BASE_URL

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
ALLURE_ENVIRONMENT_PROPERTIES_FILE = 'environment.properties'
ALLUREDIR_OPTION = '--alluredir'

# -----------------------------------------------------------------------------
# LOCAL UTILITIES
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
@pytest.fixture(scope="class")
def db_class(request):
    class DummyDB:
        pass

    # set a class attribute on the invoking test context
    request.cls.db = DummyDB()


@pytest.fixture
def getDriver(request):
    global driver
    print("browser from getDriver method - " + BROWSER)
    if BROWSER == "edge":
        edge_options = EdgeOptions()
        edge_options.add_argument("--ignore-certificate-errors")
        edge_options.add_argument("--ignore-ssl-errors")
        edge_options.add_argument("--ignore-certificate-errors-spki-list")
        # edge_options.add_argument("--headless")  # Runs in headless mode
        edge_options.add_argument("--no-sandbox")  # Bypass OS security model
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--start-fullscreen")
        edge_options.add_argument("--disable-gpu")
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=edge_options
        )
    elif BROWSER == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--disable-extensions")
        firefox_options.add_argument("--ignore-certificate-errors")
        firefox_options.add_argument("--ignore-ssl-errors")
        firefox_options.add_argument("--ignore-certificate-errors-spki-list")
        firefox_options.add_argument("--foreground")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=firefox_options
        )
    else:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--ignore-certificate-errors-spki-list")
        # chrome_options.add_argument("--headless")  # Runs in headless mode
        chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--start-fullscreen")
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
    yield driver
    time.sleep(2)
    driver.quit()


# https://github.com/allure-framework/allure-python/issues/96#issuecomment-595783149
@fixture(scope='session', autouse=True)
def add_allure_environment_property(request: SubRequest) -> Optional[Callable]:

    environment_properties = dict()

    def maker(key: str, value: Any):
        environment_properties.update({key: value})

    yield maker

    alluredir = request.config.getoption(ALLUREDIR_OPTION)

    if not alluredir or not path.isdir(alluredir) or not environment_properties:
        return

    allure_env_path = path.join(alluredir, ALLURE_ENVIRONMENT_PROPERTIES_FILE)

    with open(allure_env_path, 'w') as _f:
        data = '\n'.join([f'{variable}={value}' for variable, value in environment_properties.items()])
        _f.write(data)


@fixture(autouse=True)
def create_env_prop(add_allure_environment_property: Callable, getDriver) -> None:
    add_allure_environment_property('Env', 'Recette')
    add_allure_environment_property('Host', BASE_URL)
    driver_capabilities = getDriver.capabilities
    for key, value in driver_capabilities.items():
        add_allure_environment_property(key, value)
