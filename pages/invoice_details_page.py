from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.retry import retry_on_exception
from utils.date_picker import DatePicker
from config.settings import DEFAULT_SLEEP_TIME
import logging
import time
from selenium.webdriver.support import expected_conditions as EC
logger = logging.getLogger(__name__)

class InvoiceDetailsPage(BasePage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)
        self.date_picker = DatePicker(driver, wait)

    # Locators
    APPLY_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Apply')]]")
    DOWNLOAD_BUTTONS = (By.XPATH, "//tbody//tr//td[not(contains(@class, 'collapse-cell'))]//button[contains(@class, 'rw-button--outlined')]//i[contains(@class, 'fa-download')]/..")
    CSV_DOWNLOAD_OPTION = (By.XPATH, "//ul[contains(@class, 'dropdown-menu') and contains(@style, 'display: block')]//a[.//label-details[contains(text(), 'csv')]]")
    TABLE_ROWS = (By.CSS_SELECTOR, "tr.md-table-row")
    
    @retry_on_exception()
    def set_date_range(self, start_date, end_date):
        """Set date range and click Apply button"""
        logger.info(f"Setting date range from {start_date} to {end_date}")
        self.date_picker.set_date_range(start_date, end_date)
        time.sleep(DEFAULT_SLEEP_TIME)
        
        logger.info("Clicking Apply button...")
        apply_start = time.time()
        self.click_element(self.APPLY_BUTTON)
        logger.info("Apply button clicked")
        time.sleep(DEFAULT_SLEEP_TIME)

        # Wait for table rows to appear
        logger.info("Waiting for table rows to load...")
        try:
            rows = self.find_elements(self.TABLE_ROWS)
            logger.info(f"Found {len(rows)} table rows in {time.time() - apply_start:.2f} seconds")
        except Exception as e:
            logger.warning(f"Table rows check failed: {str(e)}")
        
        logger.info("Date range applied")

    def has_no_results(self):
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

    @retry_on_exception()
    def download_invoices(self):
        """Download available invoices"""
        if self.has_no_results():
            logger.info("No invoices found to download")
            return False
        
        try:
            logger.info("Starting invoice downloads...")
            download_buttons = self.find_elements(self.DOWNLOAD_BUTTONS)
            logger.info(f"Found {len(download_buttons)} invoices to download")
            
            for button in download_buttons:
                self.driver.execute_script("arguments[0].click();", button)
                self.click_element(self.CSV_DOWNLOAD_OPTION, sleep_after=1)
            
            return True
        except Exception as e:
            logger.error(f"Error downloading invoices: {str(e)}")
            return False