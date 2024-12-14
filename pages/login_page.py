from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.url = "https://txs.lotteryservices.com/RetailerWizard/#/home"

    # Locators
    EMAIL_INPUT = (By.NAME, "loginEmail")
    PASSWORD_INPUT = (By.NAME, "passwdRetailer")
    LOGIN_BUTTON = (By.XPATH, "//button[.//translate[text()='Log In']]")

    def navigate_to(self):
        self.driver.get(self.url)

    def login(self, email, password):
        email_input = self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
        password_input = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))

        email_input.send_keys(email)
        password_input.send_keys(password)
        login_button.click()
