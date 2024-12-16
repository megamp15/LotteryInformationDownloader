from pages.base_page import BasePage
from utils.retry import retry_on_exception
from selenium.webdriver.common.by import By
from config.settings import BASE_URL

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.NAME, "loginEmail")
    PASSWORD_INPUT = (By.NAME, "passwdRetailer")
    LOGIN_BUTTON = (By.XPATH, "//button[.//translate[text()='Log In']]")

    def navigate_to(self):
        self.driver.get(f"{BASE_URL}/home")

    @retry_on_exception()
    def login(self, email, password):
        self.find_element(self.EMAIL_INPUT).send_keys(email)
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        self.click_element(self.LOGIN_BUTTON)
