import os
import logging
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_css_when_visible(driver, wait_time, css_selector):
    element = WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
    )
    element.click()

def wait_until_css_visible(driver, wait_time, element_tuple):
    """Wait until the element specified by the CSS selector is visible."""
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(element_tuple)
        )
        return element
    except TimeoutException:
        print(f"Element with CSS selector '{element_tuple}' not visible after {wait_time} seconds.")
        return None

def scroll_to_element_and_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.execute_script("arguments[0].click();", element)


def get_element_attributes_info(driver, element, attribute = None):
    attributes = driver.execute_script(
        'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',
        element)
    if attribute is None:
        return attributes
    else:
        return attributes[attribute]


def get_cv_path(department = 'R&D', filename = 'example_cv.pdf'):
    """Get the path to the example CV file that works across OS platforms"""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the CV file
    cv_path = os.path.join(script_dir, '..', 'resources', 'cv_storage', department, filename)

    # Normalize the path to ensure it is correct for the current OS
    cv_path = os.path.normpath(cv_path)

    logging.info(f"CV path: {cv_path}")
    print({"cv_path": cv_path})
    logging.info(f"CV file exists: {os.path.exists(cv_path)}")
    print({"cv_file_exists": os.path.exists(cv_path)})

    return cv_path

