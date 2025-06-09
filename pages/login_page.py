import time
import logging
from pages.base_page import BasePage
from utils.retry import retry_on_exception
from selenium.webdriver.common.by import By
from config.settings import BASE_URL
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.NAME, "loginEmail")
    PASSWORD_INPUT = (By.NAME, "passwdRetailer")
    LOGIN_BUTTON = (By.XPATH, "//button[.//translate[text()='Log In']]")
    ERROR_MODAL = (By.XPATH, "//p[contains(text(), 'Incorrect credentials. Please try again.')]")

    def navigate_to(self):
        self.driver.get(f"{BASE_URL}/home")

    @retry_on_exception()
    def login(self, email, password):
        self.find_element(self.EMAIL_INPUT).send_keys(email)
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        self.click_element(self.LOGIN_BUTTON)

        time.sleep(3)
           
        try:
            # Check if the "Incorrect credentials" modal appeared
            error_element = self.driver.find_element(*self.ERROR_MODAL)
            if error_element.is_displayed():
                logger.error(f"Login failed for {email}: Incorrect credentials modal displayed")
                return False
        except NoSuchElementException:
            # No error modal found, login likely successful
            pass
