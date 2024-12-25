from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from config.settings import DEFAULT_WAIT_TIME
import time
import logging

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver, wait=None):
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, DEFAULT_WAIT_TIME)

    # Common locators
    TABLE_ROWS = (By.CSS_SELECTOR, "tr.md-table-row")

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

    def has_no_results(self):
        """Check if the page has no results by examining table rows and no-results message"""
        logger.info("Checking for no results...")
        
        # Check table rows
        rows = self.find_elements(self.TABLE_ROWS)
        row_count = len(rows)
        logger.info(f"Found {row_count} rows")
        
        if row_count > 1:
            logger.info("Multiple rows found - has results")
            return False
        elif row_count == 1:
            # If only one row, verify it's not just showing "no results"
            no_results_locator = (By.XPATH, "//div[contains(text(), 'Sorry, no results were found.')]")
            if self.is_element_present(no_results_locator):
                logger.info("Single row with 'no results' message found")
                return True
            else:
                logger.info("Single row with actual data found")
                return False
        else:
            logger.info("No rows found")
            return True 