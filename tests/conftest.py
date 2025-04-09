import datetime
import logging
import platform
import time
from os import path
from typing import Any, Callable, Optional

import pytest
from _pytest.fixtures import SubRequest
from decouple import config
from pytest import fixture
from selenium import webdriver
from utils.constants import Constant as CONST
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from pages.careers_page import CareersPage
# Our own imports ---------------------------------------------------
from pages.home_page import HomePage

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
ALLURE_ENVIRONMENT_PROPERTIES_FILE = 'environment.properties'
ALLUREDIR_OPTION = '--alluredir'

# -----------------------------------------------------------------------------
# Configure logging
# -----------------------------------------------------------------------------
# Create a custom logger
logger = logging.getLogger(__name__)
# Set log level
logger.setLevel(logging.INFO)
# Configure handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# Create formatter
console_format = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s', 
                                   datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(console_format)
# Add handler
logger.addHandler(console_handler)

# -----------------------------------------------------------------------------
# Allure Reporting Fixtures
# -----------------------------------------------------------------------------
@fixture(scope='session', autouse=True)
def add_allure_environment_property(request: SubRequest) -> Optional[Callable]:
    """Add environment properties to Allure report"""
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
def create_env_prop(add_allure_environment_property: Callable, request, base_url, driver) -> None:
    """Add environment properties to Allure report from driver capabilities"""
    try:
        add_allure_environment_property('Env', 'Testing')
        add_allure_environment_property('Host', base_url)
        add_allure_environment_property('Platform', platform.platform())
        add_allure_environment_property('Python', platform.python_version())
        
        # Add driver capabilities to environment properties
        for key, value in driver.capabilities.items():
            add_allure_environment_property(key, value)
    except Exception as e:
        logger.warning(f"Could not add environment properties: {e}")

@pytest.fixture(autouse=True)
def add_timestamp_to_test_name(request):
    """Add timestamp to test name for unique test runs"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    original_name = request.node.name
    request.node.name = f"{original_name}_{timestamp}"
    request.node.originalname = original_name

# -----------------------------------------------------------------------------
# Configuration fixtures
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def base_url():
    """Return the base URL for tests."""
    return config('CONNECTEAM_URL', default=CONST.HOME_PAGE)

@pytest.fixture(scope="session")
def browser_type():
    """Return the browser to use for testing."""
    return config('BROWSER', default='chrome')

# -----------------------------------------------------------------------------
# WebDriver fixtures
# -----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def driver(browser_type, base_url, request):
    """
    Create and configure WebDriver.
    Scope="function" means this runs for each test function.
    Enhanced to support parametrized tests with better parallel execution.
    """
    logger.info(f"Setting up {browser_type} browser")
    
    # Get test name and parameters for better logging and identification
    test_name = request.node.name
    
    # Create a unique session ID for this test instance to avoid conflicts in parallel runs
    session_id = f"{test_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    logger.info(f"Starting test with session ID: {session_id}")
    
    if browser_type == "edge":
        # Edge configuration
        options = EdgeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--ignore-certificate-errors-spki-list")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        # Add unique user data dir to prevent conflicts in parallel runs
        options.add_argument(f"--user-data-dir=/tmp/edge_profile_{session_id}")
        
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    elif browser_type == "firefox":
        # Firefox configuration
        options = FirefoxOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--ignore-certificate-errors-spki-list")
        options.add_argument("--foreground")
        # Add unique profile path for Firefox
        options.add_argument(f"-profile")
        options.add_argument(f"/tmp/firefox_profile_{session_id}")
        
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    else:
        # Chrome configuration (default)
        options = ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--ignore-certificate-errors-spki-list")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-gpu')
        # Add unique user data dir to prevent conflicts in parallel runs
        options.add_argument(f"--user-data-dir=/tmp/chrome_profile_{session_id}")
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    # Configure WebDriver with longer timeouts for better stability
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(20)
    driver.maximize_window()
    
    # Navigate to base URL
    driver.get(base_url)
    logger.info(f"Navigated to {base_url}")
    
    # Store session info for debugging
    request.node.session_id = session_id
    
    # Yield driver to test
    yield driver
    
    # Cleanup after test
    logger.info(f"Tearing down WebDriver for session {session_id}")
    try:
        driver.quit()
    except Exception as e:
        logger.warning(f"Error during driver cleanup: {e}")

# -----------------------------------------------------------------------------
# Page Object fixtures
# -----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def home_page(driver):
    """Return a HomePage object."""
    logger.info("Creating HomePage object")
    # Wait for homepage to be fully loaded before returning
    home_page = HomePage(driver)
    # Explicitly wait for homepage to be ready
    home_page.wait_for_page_load()
    return home_page

@pytest.fixture(scope="function")
def careers_page(driver, base_url):
    """Return a CareersPage object."""
    logger.info("Creating CareersPage object")
    driver.get(f"{base_url}careers/")
    careers_page = CareersPage(driver)
    # Wait for page to be fully loaded
    time.sleep(2)  # Give a moment for the page to stabilize
    return careers_page