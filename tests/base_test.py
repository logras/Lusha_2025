
import unittest

# Third-party imports -----------------------------------------------
import pytest
# import xmlrunner
import HtmlTestRunner
from decouple import config
from selenium import webdriver
from utils.constants import Constant as CONST

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


BASE_URL = config('CONNECTEAM_URL', default=CONST.HOME_PAGE)
BROWSER = config('BROWSER', default='chrome')


class BaseTest(unittest.TestCase):

    browser = BROWSER

    def setUp(self):
        if self.browser == "edge":
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
            self.driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=edge_options
            )
        elif self.browser == "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--disable-extensions")
            firefox_options.add_argument("--ignore-certificate-errors")
            firefox_options.add_argument("--ignore-ssl-errors")
            firefox_options.add_argument("--ignore-certificate-errors-spki-list")
            firefox_options.add_argument("--foreground")
            self.driver = webdriver.Firefox(
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
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=chrome_options
            )

        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(BASE_URL)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover('.')
    HtmlTestRunner.HTMLTestRunner(combine_reports=True, output='reports/html').run(suite)
