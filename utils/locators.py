from selenium.webdriver.common.by import By


class HomePageLocators(object):
    def __init__(self, param=None):
        self.CAREERS_BUTTON = (By.CSS_SELECTOR, "a[href='/careers/']")

        # Page verification
        self. CAREERS_HEADING = (By.XPATH, "//h1[contains(text(), 'Career')]")
        self.PAGE_CONTENT = (By.CSS_SELECTOR, "div.careers-page")


        # Application form elements
        self.APPLICATION_FORM = (By.CSS_SELECTOR, "div.apply-form")
        self.FIRST_NAME_FIELD = (By.NAME, "firstName")
        self.LAST_NAME_FIELD = (By.NAME, "lastName")
        self.EMAIL_FIELD = (By.NAME, "email")
        self.PHONE_FIELD = (By.NAME, "phone")
        self.CV_UPLOAD_FIELD = (By.CSS_SELECTOR, "input[type='file']")
        self.CLOSE_FORM_BUTTON = (By.CSS_SELECTOR, "button.close-button")


class CareersPageLocators(object):
    def __init__(self, param=None):
        self.DEPARTMENTS_FILTER = (By.ID, "department-filter")
        self.RD_OPTION = (By.XPATH, f"//option[@value='{param}']")
        self.SELECTED_DEPARTMENT = (By.XPATH, f"//select[@id='department-filter']/option[@selected]")
        self.RND_JOB_CARDS = (By.CSS_SELECTOR, f"""[role="row"][data-department="{param}"] td[class="link"] a""")
        # self.driver.find_elements(By.CSS_SELECTOR, '[role="row"][data-department="R&D"] td[class="link"] a')[5].text
        self.APPLY_NOW_BUTTONS = (
        By.XPATH, "//a[contains(@class, 'apply-button') and contains(text(), 'Apply Now')]")
        self.BACK_TO_ALL_CAREERS_BUTTON = (By.CSS_SELECTOR, """.section-careers-single-back""")
        self.FILTER_SECTION = (By.CSS_SELECTOR, "div.filter-wrapper")

class PositionPageLocators(object):
    def __init__(self, param=None):

        self.POSITION_FORM_CV_INPUT = (By.ID, "resume")
        self.POSITION_FORM_CV_VALIDATION = (By.CSS_SELECTOR, "[class='body body__secondary']")
        self.CV_UPLOAD_FIELD = (By.CSS_SELECTOR, "input[type='file']")

        self.POSITION_FORM_IFRAME = (By.ID, 'grnhse_iframe')
        self.POSITION_FORM_FIRST_NAME = (By.ID, 'first_name')
        self.POSITION_FORM_LAST_NAME = (By.ID, 'last_name')
        self.POSITION_FORM_EMAIL = (By.ID, 'email')
        self.POSITION_FORM_PHONE = (By.ID, 'phone')
        self.POSITION_FORM_SEARCH = (By.ID, 'id=keyword-filter-label')
        self.POSITION_DESCRIPTION = (By.CSS_SELECTOR, "div.job-description")
        self.POSITION_DEPARTMENT = (By.XPATH, f"//span[contains(text(), '{param}')]")
        self.APPLY_NOW_BUTTON = (By.XPATH, "//a[contains(@class, 'apply-button') and contains(text(), 'Apply Now')]")
        self.BACK_TO_ALL_CAREERS_BUTTON = (By.CSS_SELECTOR, """.section-careers-single-back""")

class LoginPageLocators(object):
    EMAIL = (By.XPATH, '//*[@id="login"]')
    PASSWORD = (By.XPATH, '//*[@id="password"]')
    # SUBMIT = (By.XPATH, '//*[@id="app"]/div[1]/div/div/div/div/div/div/div/form/button')
    SUBMIT = (By.XPATH, '/html/body/div[1]/div[1]/div/div/div/div/div/div/div/form/button')
    # ERROR_MESSAGE = (By.ID, 'message_error')
    ERROR_MESSAGE = (By.XPATH, '//*[@id="app"]/div[1]/div/div/div/div/div/div/div/form/div[1]/div[1]/p')
