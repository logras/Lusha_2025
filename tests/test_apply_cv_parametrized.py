import logging

import allure
import pytest
from pages.careers_page import CareersPage
from utils.constants import Constant as CONST

LOGGER = logging.getLogger(__name__)

# Test data for different departments and candidate profiles
test_data = [
    # Department, Candidate Details
    ("R&D", {
        'first_name': CONST.TEST_FIRST_NAME,
        'last_name': CONST.TEST_LAST_NAME,
        'email': CONST.TEST_EMAIL,
        'phone': CONST.TEST_PHONE
    }),
    ("G&A", {
        'first_name': CONST.TEST_FIRST_NAME,
        'last_name': CONST.TEST_LAST_NAME,
        'email': CONST.TEST_EMAIL,
        'phone': CONST.TEST_PHONE
    })
]

@allure.epic("Careers Page Testing")
@allure.feature("Job Application Process")
class TestParametrizedApplications:
    """Test applying to jobs on the Connecteam careers page with parametrized data."""

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    @pytest.mark.nondestructive
    @pytest.mark.parametrize("department_name, candidate_details", test_data, ids=lambda d: f"{d}")
    def test_apply_cv_to_department(self, driver, home_page, department_name, candidate_details):
        """
        Test applying for positions in different departments on Connecteam careers page.
        
        This parametrized test will apply to all openings in the selected departments,
        using different candidate profiles for each department. The test covers:
        
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
        LOGGER.info(f"\n=== Step 3: Selecting {department_name} Department ===")
        careers_page = CareersPage(driver)
        careers_page.select_department(department_name), "Failed to select R&D department"

        # Step 4: Apply for all positions in R&D department
        LOGGER.info("\n=== Step 4: Applying CVs to all open positions ===")
        careers_page.apply_to_all_the_openings_per_department(department_name=department_name, candidate_details=candidate_details)
