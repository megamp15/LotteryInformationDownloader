from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.settings import DEFAULT_WAIT_TIME
import time

class BasePage:
    def __init__(self, driver, wait=None):
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, DEFAULT_WAIT_TIME)

    def click_element(self, locator, sleep_after=0):
        """Safe click with JavaScript executor"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", element)
        if sleep_after:
            time.sleep(sleep_after)

    def find_element(self, locator):
        """Find element with wait"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Find elements with wait"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def is_element_present(self, locator):
        """Check if element is present"""
        try:
            self.find_element(locator)
            return True
        except:
            return False 