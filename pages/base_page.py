import time
import logging
import decouple

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException, 
    StaleElementReferenceException,
    NoSuchElementException,
    NoSuchWindowException,
    WebDriverException
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
BASE_URL = decouple.config('CONNECTEAM_URL')
LOGGER = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
# Default timeout values
DEFAULT_TIMEOUT = 30
SHORT_TIMEOUT = 10
LONG_TIMEOUT = 60

class BasePage(object):
    """
    Base class for all page objects in the framework.
    Provides common methods for interacting with pages.
    """
    def __init__(self, driver, base_url=BASE_URL):
        self.base_url = base_url
        self.driver = driver
        self.timeout = DEFAULT_TIMEOUT
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def find_element(self, *locator):
        """Find an element with appropriate error handling."""
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException as e:
            self.logger.error(f"Element not found with locator: {locator}")
            raise e

    def find_elements(self, *locator):
        """Find multiple elements with appropriate error handling."""
        try:
            elements = self.driver.find_elements(*locator)
            self.logger.debug(f"Found {len(elements)} elements with locator: {locator}")
            return elements
        except NoSuchElementException as e:
            self.logger.error(f"No elements found with locator: {locator}")
            return []

    def open(self, url):
        """Open a URL, handling potential errors."""
        try:
            full_url = self.base_url + url
            self.logger.info(f"Opening URL: {full_url}")
            self.driver.get(full_url)
            self.wait_for_page_load()
        except WebDriverException as e:
            self.logger.error(f"Failed to open URL: {url}. Error: {str(e)}")
            raise e

    def get_title(self):
        """Get page title with error handling."""
        try:
            return self.driver.title
        except WebDriverException as e:
            self.logger.error(f"Failed to get page title: {str(e)}")
            return ""

    def get_url(self):
        """Get current URL with error handling."""
        try:
            return self.driver.current_url
        except WebDriverException as e:
            self.logger.error(f"Failed to get current URL: {str(e)}")
            return ""

    def hover(self, *locator):
        """Hover over an element with error handling and retries."""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                element = self.find_element(*locator)
                self.logger.debug(f"Hovering over element: {locator}")
                hover = ActionChains(self.driver).move_to_element(element)
                hover.perform()
                return True
            except (StaleElementReferenceException, NoSuchElementException) as e:
                if attempt < max_attempts - 1:
                    self.logger.warning(f"Retry {attempt+1}/{max_attempts} hovering over element: {locator}")
                    time.sleep(1)
                else:
                    self.logger.error(f"Failed to hover over element after {max_attempts} attempts: {str(e)}")
                    raise e

    def wait_element(self, *locator, timeout=None):
        """Wait for an element to be present with robust error handling."""
        timeout = timeout or self.timeout
        try:
            self.logger.debug(f"Waiting for element: {locator} (timeout: {timeout}s)")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found within {timeout} seconds: {locator}")
            # Take screenshot for debugging
            try:
                screenshot_path = f"screenshots/element_not_found_{time.time()}.png"
                self.driver.save_screenshot(screenshot_path)
                self.logger.info(f"Screenshot saved to {screenshot_path}")
            except Exception as e:
                self.logger.warning(f"Could not take screenshot: {str(e)}")
            raise TimeoutException(f"Element not found within {timeout} seconds: {locator}")

    def wait_for_element_visible(self, *locator, timeout=None):
        """Wait for an element to be visible on the page."""
        timeout = timeout or self.timeout
        try:
            self.logger.debug(f"Waiting for element to be visible: {locator} (timeout: {timeout}s)")
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible within {timeout} seconds: {locator}")
            raise TimeoutException(f"Element not visible within {timeout} seconds: {locator}")

    def wait_for_element_clickable(self, *locator, timeout=None):
        """Wait for an element to be clickable."""
        timeout = timeout or self.timeout
        try:
            self.logger.debug(f"Waiting for element to be clickable: {locator} (timeout: {timeout}s)")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable within {timeout} seconds: {locator}")
            raise TimeoutException(f"Element not clickable within {timeout} seconds: {locator}")

    def wait_for_page_load(self, timeout=LONG_TIMEOUT):
        """
        Wait for the page to be fully loaded.
        This method uses document.readyState to determine if the page is complete.
        """
        try:
            self.logger.debug(f"Waiting for page to load (timeout: {timeout}s)")
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            # Additional wait for AJAX requests to complete
            time.sleep(1)
            self.logger.debug("Page fully loaded")
            return True
        except TimeoutException:
            self.logger.error(f"Page not loaded within {timeout} seconds")
            return False
        except WebDriverException as e:
            self.logger.error(f"Error waiting for page load: {str(e)}")
            return False

    def safe_click(self, *locator, timeout=None):
        """
        Safely click an element with retries and waits.
        Handles StaleElementReferenceException and other common exceptions.
        """
        timeout = timeout or self.timeout
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                element = self.wait_for_element_clickable(*locator, timeout=timeout)
                self.logger.debug(f"Clicking element: {locator}")
                element.click()
                return True
            except (StaleElementReferenceException, NoSuchElementException, WebDriverException) as e:
                if attempt < max_attempts - 1:
                    self.logger.warning(f"Retry {attempt+1}/{max_attempts} clicking element: {locator}")
                    time.sleep(1)
                else:
                    self.logger.error(f"Failed to click element after {max_attempts} attempts: {str(e)}")
                    # Try JavaScript click as a fallback
                    try:
                        element = self.find_element(*locator)
                        self.logger.debug("Attempting JavaScript click as fallback")
                        self.driver.execute_script("arguments[0].click();", element)
                        return True
                    except Exception as js_error:
                        self.logger.error(f"JavaScript click also failed: {str(js_error)}")
                        raise e

    def is_element_present(self, *locator, timeout=SHORT_TIMEOUT):
        """Check if an element is present on the page."""
        try:
            self.wait_element(*locator, timeout=timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_visible(self, *locator, timeout=SHORT_TIMEOUT):
        """Check if an element is visible on the page."""
        try:
            self.wait_for_element_visible(*locator, timeout=timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def safe_send_keys(self, *locator, text, clear_first=True, timeout=None):
        """Safely send keys to an element with proper waits and error handling."""
        timeout = timeout or self.timeout
        try:
            element = self.wait_for_element_visible(*locator, timeout=timeout)
            if clear_first:
                element.clear()
            self.logger.debug(f"Sending text to element: {locator}")
            element.send_keys(text)
            return True
        except (StaleElementReferenceException, NoSuchElementException, WebDriverException) as e:
            self.logger.error(f"Failed to send keys to element: {str(e)}")
            raise e

    def safe_get_text(self, *locator, timeout=None):
        """Safely get text from an element with proper waits and error handling."""
        timeout = timeout or self.timeout
        try:
            element = self.wait_for_element_visible(*locator, timeout=timeout)
            return element.text
        except (StaleElementReferenceException, NoSuchElementException, WebDriverException) as e:
            self.logger.error(f"Failed to get text from element: {str(e)}")
            return ""

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
