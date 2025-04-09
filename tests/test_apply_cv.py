import logging
import allure
import pytest
from pages.careers_page import CareersPage
from utils.constants import Constant as CONST

LOGGER = logging.getLogger(__name__)

candidate_details = {'first_name': CONST.TEST_FIRST_NAME, 'last_name': CONST.TEST_LAST_NAME, 'email': CONST.TEST_EMAIL, 'phone': CONST.TEST_PHONE}


@allure.testcase(CONST.HOME_PAGE, 'Home page')
class TestHomePage:
    """Test applying to jobs on the Connecteam careers page."""

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    @pytest.mark.nondestructive
    def test_apply_cv_to_rnd(self, driver, home_page):
        """Test applying for R&D positions on Connecteam careers page,
        this test will apply to all the openings in the selected department, covering the following steps:
        1. Navigate to connecteam.com
        2. Scroll and click careers in footer
        3. Select R&D from dropdown
        4. Apply for all positions"""

        # Step 1: Initialize home page and verify it's loaded
        LOGGER.info("\n=== Step 1: Verifying Home Page ===")
        home_page.check_homepage_page_loaded()

        # Step 2: Navigate to careers page
        LOGGER.info("\n=== Step 2: Navigating to Careers Page ===")
        home_page.click_careers_button()

        # Step 3: Initialize careers page and select R&D department
        LOGGER.info("\n=== Step 3: Selecting R&D Department ===")
        careers_page = CareersPage(driver)
        careers_page.select_department("R&D"), "Failed to select R&D department"

        # Step 4: Apply for all positions in R&D department
        LOGGER.info("\n=== Step 4: Applying CVs to all open positions ===")
        careers_page.apply_to_all_the_openings_per_department(department_name="R&D", candidate_details=candidate_details)
