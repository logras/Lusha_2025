import allure
import time
import os
import platform
import logging

from selenium.webdriver.remote.remote_connection import LOGGER

import utils.helpers
from utils.helpers import *
from utils.constants import Constant as CONST
# Third-party imports -----------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchWindowException, StaleElementReferenceException

# Our own imports ---------------------------------------------------
from pages.base_page import BasePage
from pages.position_page import PositionPage
from utils.locators import CareersPageLocators, HomePageLocators
from utils.decorators import time_func


timeout = 60
# -----------------------------------------------------------------------------
class CareersPage(BasePage):
    def __init__(self, driver):
        self.locator = CareersPageLocators
        super().__init__(driver)  # Python3 version
        self.position_page = PositionPage(driver)
        self.logger = logging.getLogger(__name__)
        LOGGER = self.logger

    @time_func
    # @allure.step("Apply to all the openings in the selected department")
    def apply_to_all_the_openings_per_department(self, department_name, candidate_details):
        """Apply to all the openings in the selected department
        This test will apply to all the openings in the selected department"""
        ELEMENT = CareersPageLocators(param=department_name)
        try:
            self.logger.info("Trying to search for jobs with R&D in the title")
            # Wait for page to be fully loaded after selection
            self.wait_for_page_load()
            
            # Use our enhanced wait methods
            with allure.step(f"Finding job cards for {department_name}"):
                # Use find_elements with better error handling
                rnd_job_cards = self.find_elements(*ELEMENT.RND_JOB_CARDS)
                self.logger.info(f"Found {len(rnd_job_cards)} job cards on the page")
                
                # Take screenshot for debugging
                try:
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(
                        screenshot,
                        name=f"{department_name}_Jobs_Found",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as e:
                    self.logger.warning(f"Could not take screenshot: {e}")
            
            # Process each job card
            for i in range(len(rnd_job_cards)):
                # Re-find elements to avoid stale references in parallel execution
                try:
                    rnd_job_cards = self.find_elements(*ELEMENT.RND_JOB_CARDS)
                    if i >= len(rnd_job_cards):
                        self.logger.warning(f"Job card index {i} is out of range. Total cards: {len(rnd_job_cards)}")
                        break
                        
                    self.logger.info(f"Job card {i}: {rnd_job_cards[i].text}")
                    
                    # Process card if it has "Apply now" text
                    if rnd_job_cards[i].text == "Apply now":
                        with allure.step(f"Processing job card {i} with 'Apply now'"):
                            # Get the URL safely
                            card_url = utils.helpers.get_element_attributes_info(
                                self.driver, element=rnd_job_cards[i], attribute='href'
                            )
                            self.logger.info(f"Found URL in job card: {card_url}")
                            
                            # Scroll and click with enhanced method
                            scroll_to_element_and_click(self.driver, rnd_job_cards[i])
                            
                            # Wait for page load and verify URL
                            self.wait_for_page_load()
                            current_url = self.get_url()
                            self.logger.info(f"Current URL: {current_url}")
                            
                            # Verify we're on the right page
                            assert card_url in current_url, f"Expected URL: {card_url}, but got: {current_url}"

                            # Fill the application form
                            self.logger.info("\n=== Step 4: Filling Out Application Form ===")
                            self.position_page.fill_up_position_form(candidate_details, card_number=i, card_url=card_url)

                            # Go back to careers page
                            with allure.step("Returning to careers page"):
                                self.driver.get(CONST.CAREERS_PAGE)
                                self.logger.info(f"Navigated back to {CONST.CAREERS_PAGE}")
                                # Wait for careers page to load
                                self.wait_for_page_load()
                                
                                # Reselect department
                                self.select_department(department_name)
                    else:
                        self.logger.info("Job card has no 'Apply now' text on page")
                except (StaleElementReferenceException, NoSuchElementException) as e:
                    self.logger.warning(f"Element became stale or disappeared during processing: {e}")
                    # Try to recover by refreshing the department selection
                    try:
                        self.driver.get(CONST.CAREERS_PAGE)
                        self.wait_for_page_load()
                        self.select_department(department_name)
                    except Exception as recover_error:
                        self.logger.error(f"Could not recover from stale element: {recover_error}")
                except NoSuchWindowException as e:
                    self.logger.error(f"Window was closed unexpectedly: {e}")
                    # Try to recover by creating a new window
                    try:
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        self.driver.get(CONST.CAREERS_PAGE)
                        self.wait_for_page_load()
                        self.select_department(department_name)
                    except Exception as window_error:
                        self.logger.error(f"Could not recover from closed window: {window_error}")
                        raise e
                except Exception as e:
                    self.logger.error(f"Error processing job card {i}: {e}")
                    # Take screenshot for debugging
                    try:
                        screenshot = self.driver.get_screenshot_as_png()
                        allure.attach(
                            screenshot,
                            name=f"Error_Job_Card_{i}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    except Exception as screenshot_error:
                        self.logger.warning(f"Could not take error screenshot: {screenshot_error}")

        except Exception as e:
            self.logger.error(f"Error in clicking job card: {e}")
            # Take screenshot for debugging
            try:
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="Error_Department_Processing",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as screenshot_error:
                self.logger.warning(f"Could not take error screenshot: {screenshot_error}")
            raise e


    @allure.step("Select {department_name} department")
    def select_department(self, department_name):
        ELEMENT = CareersPageLocators(param=department_name)
        """Select a department from the filters"""
        try:
            # Wait for the page to fully load
            self.wait_for_page_load()
            self.logger.info(f"Selecting {department_name} department using dropdown")

            # Step 1: Find and click the department filter dropdown with enhanced methods
            with allure.step("Clicking department filter dropdown"):
                department_filter = self.wait_for_element_clickable(
                    *ELEMENT.DEPARTMENTS_FILTER, 
                    timeout=timeout
                )
                department_filter.click()
                self.logger.info("Clicked on department filter dropdown")
                # Short wait for dropdown to open
                time.sleep(1)

            # Step 2: Find and select the department option with enhanced methods
            with allure.step(f"Selecting {department_name} option"):
                department_option = self.wait_for_element_clickable(
                    *ELEMENT.RD_OPTION, 
                    timeout=timeout
                )
                # Use safe_click for better reliability
                self.safe_click(*ELEMENT.RD_OPTION, timeout=timeout)
                self.logger.info(f"Selected {department_name} option from dropdown")
            
            # Wait for filter to be applied
            time.sleep(2)
            
            # Take screenshot after selecting the department
            try:
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name=f"Selected_{department_name}_Department",
                    attachment_type=allure.attachment_type.PNG
                )
                self.logger.info(f"Screenshot of {department_name} department selection attached to Allure report")
            except Exception as screenshot_error:
                self.logger.error(f"Error attaching screenshot to Allure report: {screenshot_error}")
            
            return True
        except Exception as e:
            self.logger.error(f"Error in department selection: {e}")
            # Take screenshot for error debugging
            try:
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name=f"Error_Selecting_{department_name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as screenshot_error:
                self.logger.warning(f"Could not take error screenshot: {screenshot_error}")
            raise e