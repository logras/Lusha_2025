import allure
import time
import os
import platform

from selenium.webdriver.remote.remote_connection import LOGGER

import utils.helpers
from utils.helpers import *
from utils.constants import Constant as CONST
# Third-party imports -----------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Our own imports ---------------------------------------------------
from pages.base_page import BasePage
from utils.locators import PositionPageLocators

wait_time = 60

class PositionPage(BasePage):
    def __init__(self, driver):
        self.locator = PositionPageLocators
        super().__init__(driver)  # Python3 version
        self.logger = logging.getLogger(__name__)
        LOGGER = self.logger

    @allure.step("apply to all the openings in the selected department")
    def fill_up_position_form(self, candidate_details):
        ELEMENT = PositionPageLocators()
        """Apply to all the openings in the selected department"""

        # verify page finished loading
        self.check_page_loaded()
        # get candidate details
        # first_name = candidate_details['first_name']
        # last_name = candidate_details['last_name']
        # email = candidate_details['email']
        # phone = candidate_details['phone']

        ELEMENT = PositionPageLocators()
        try:
            LOGGER.info("Trying to fill up the position form")
            WebDriverWait(self.driver, wait_time).until(
                EC.frame_to_be_available_and_switch_to_it(ELEMENT.POSITION_FORM_IFRAME)
            )

            fields = {
                ELEMENT.POSITION_FORM_FIRST_NAME: CONST.TEST_FIRST_NAME,
                ELEMENT.POSITION_FORM_LAST_NAME: CONST.TEST_LAST_NAME,
                ELEMENT.POSITION_FORM_EMAIL: CONST.TEST_EMAIL,
                ELEMENT.POSITION_FORM_PHONE: CONST.TEST_PHONE
            }

            for locator, value in fields.items():
                field = wait_until_css_visible(self.driver, wait_time, locator)
                field.send_keys(value)
                LOGGER.info(f"Filled {locator}: {value}")

            #TODO -  self.validate_cv_upload_in_the_ui()
            #Taking screenshot of careers page before selection
            screenshot = self.driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="position_form filled up with candidate details",
                attachment_type=allure.attachment_type.PNG)
        except TimeoutException as e:
            # handling the case when the position is no longer available
            if wait_until_css_visible(self.driver, wait_time, ELEMENT.POSITION_FORM_SEARCH):
                LOGGER.info("Position is no longer available")
            else:
                raise e

        except Exception as e:
            LOGGER.error(f"Error filling up position form {e}")
            raise e

    def validate_cv_upload_in_the_ui(self):
        """Validate if CV upload was successful in the ui"""
        ELEMENT = PositionPageLocators()
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(ELEMENT.POSITION_FORM_CV_VALIDATION)
            )
            assert element.text == CONST.CV_FILE_NAME
        except TimeoutException:
            print(f"Element with CSS selector '{ELEMENT.POSITION_FORM_CV_VALIDATION}' not found after {wait_time} seconds.")
            return None

    def check_page_loaded(self, timeout=10):
        """Wait for the page to finish loading by checking the document ready state and the presence of an embedded part."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            LOGGER.info("Page has finished loading.")

            # Wait for the embedded part to be present
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job__embedded-wrapper"))
            )
        except TimeoutException:
            LOGGER.info("Timed out waiting for page to load or embedded part to be present.")
        finally:
            # Print the current document.readyState
            ready_state = self.driver.execute_script('return document.readyState')
            LOGGER.info(f"Current document.readyState: {ready_state}")
