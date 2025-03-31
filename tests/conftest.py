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
import inspect
import datetime

from os import path
from typing import Any, Callable, Optional

# Third-party imports -----------------------------------------------
import pytest
import logging

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

# Create a custom logger
logger = logging.getLogger(__name__)

# Set the global log level
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')

# Set log levels for handlers
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add them to handlers
console_format = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_format = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(filename)s - %(lineno)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(console_handler)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


@pytest.fixture(scope="class")
def db_class(request):
    class DummyDB:
        pass

    # set a class attribute on the invoking test context
    request.cls.db = DummyDB()


@pytest.fixture
def getDriver(request):
    # Check if this is being called from a unittest test
    # In that case, we'll use the driver from the unittest test
    for frame in inspect.stack():
        if 'unittest' in frame.filename:
            # Get the unittest test instance
            test_instance = frame.frame.f_locals.get('self')
            if test_instance and hasattr(test_instance, 'driver'):
                # Return the driver from the unittest test
                print("Using driver from unittest")
                yield test_instance.driver
                return
    
    # If not called from unittest, create a new driver
    global driver
    print("Creating new driver from getDriver method - " + BROWSER)
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
def create_env_prop(add_allure_environment_property: Callable, request) -> None:
    # Check if this is being called from a unittest test
    is_unittest = False
    for frame in inspect.stack():
        if 'unittest' in frame.filename:
            is_unittest = True
            # Get the unittest test instance
            test_instance = frame.frame.f_locals.get('self')
            if test_instance and hasattr(test_instance, 'driver'):
                # Use the driver from the unittest test for environment properties
                add_allure_environment_property('Env', 'Recette')
                add_allure_environment_property('Host', BASE_URL)
                driver = test_instance.driver
                for key, value in driver.capabilities.items():
                    add_allure_environment_property(key, value)
                break
    
    # If not called from unittest, use the getDriver fixture
    if not is_unittest:
        from pytest import FixtureRequest
        request: FixtureRequest
        driver = request.getfixturevalue('getDriver')
        add_allure_environment_property('Env', 'Recette')
        add_allure_environment_property('Host', BASE_URL)
        for key, value in driver.capabilities.items():
            add_allure_environment_property(key, value)



@pytest.fixture(autouse=True)
def add_timestamp_to_test_name(request):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    original_name = request.node.name
    request.node.name = f"{original_name}_{timestamp}"
    request.node.originalname = original_name