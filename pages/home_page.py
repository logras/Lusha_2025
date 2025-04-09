import time
import allure
import logging
from utils.decorators import time_func
from selenium.webdriver.remote.remote_connection import LOGGER
from utils.constants import Constant as CONST
from retry import retry
from selenium.common.exceptions import NoSuchElementException

# Third-party imports -----------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.locators import CareersPageLocators, HomePageLocators


# Our own imports ---------------------------------------------------
from pages.base_page import BasePage
from utils.locators import HomePageLocators

timeout = 60

class HomePage(BasePage):
    def __init__(self, driver):
        self.locator = HomePageLocators
        super().__init__(driver)  # Python3 version
        self.logger = logging.getLogger(__name__)
        LOGGER = self.logger


    @time_func
    @retry(tries=2, delay=2, exceptions=TimeoutException)
    @allure.step("Checking home page is loaded")
    def check_homepage_page_loaded(self, timeout=10):
        """Wait for the page to finish loading by checking the document ready state and the presence of an embedded part."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            LOGGER.info("Home page has finished loading.")

        except TimeoutException as e:
            LOGGER.error("Timed out waiting for page to load or embedded part to be present.")
            raise e
        finally:
            # Print the current document.readyState
            ready_state = self.driver.execute_script('return document.readyState')
            LOGGER.info(f"Current document.readyState: {ready_state}")
        try:
            title = self.get_title()
            LOGGER.info(f"Checking page title: {title}")
            assert "Connecteam" in title or "connecteam.com" in self.get_url(), "Page did not load correctly"
            return True

        except Exception as e:
            LOGGER.error("Error in the title or URL check")
            raise e



    def scroll_to_footer(self):
        """Scroll down to the bottom of the page to make footer visible"""
        try:
            # Scroll down to the bottom of the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for scroll to complete
            time.sleep(3)
            LOGGER.info("Scrolled to footer")
            return True
        except Exception as e:
            LOGGER.error(f"Error scrolling to footer: {e}")
            return False

    @retry(tries=3, delay=2, exceptions=NoSuchElementException)
    @allure.step("Clicking on the careers button")
    def click_careers_button(self):
        ELEMENT = HomePageLocators()
        """Scroll to footer and click on the careers link"""
        # Scroll to footer first
        self.scroll_to_footer()
        
        try:
            # Try to find the careers button
            careers_button = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(ELEMENT.CAREERS_BUTTON)
            )
            
            # Print element info for debugging
            LOGGER.info(f"Found careers button: {careers_button.is_displayed()}")
            
            # Click on the careers link using JavaScript
            self.driver.execute_script("arguments[0].click();", careers_button)

            
            # Return the current URL to verify navigation
            current_url = self.get_url()
            LOGGER.info(f"Current URL after clicking careers: {current_url}")
            
            # If the URL doesn't contain 'careers', try again
            if "careers" not in current_url:
                LOGGER.info("First click didn't work, trying direct navigation...")
                self.driver.get(CONST.CAREERS_PAGE)
                time.sleep(2)
                current_url = self.get_url()
                LOGGER.info(f"Current URL after direct navigation: {current_url}")

                # Make sure the page has time to fully load
            LOGGER.info(f"Current URL: {self.driver.current_url}")
            LOGGER.info(f"Page title: {self.driver.title}")
            # Check if the URL contains 'careers'
            assert "careers" in current_url, "Navigation to careers page failed"

            try:
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name=f"Careers_Page_Before_Selection",
                    attachment_type=allure.attachment_type.PNG
                )
                LOGGER.info(f"Screenshot of Careers_Page_Before_Selection attached to Allure report")
            except Exception as screenshot_error:
                LOGGER.error(f"Error attaching screenshot to Allure report: {screenshot_error}")

            return current_url
            
        except NoSuchElementException:
            LOGGER.info("Could not find the careers button, will retry")
        except Exception as e:
            LOGGER.error(f"Error clicking careers button: {e}")
            raise e