from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.retry import retry_on_exception
from utils.date_picker import DatePicker
from config.settings import DEFAULT_SLEEP_TIME
import logging

logger = logging.getLogger(__name__)

class InvoiceDetailsPage(BasePage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)
        self.date_picker = DatePicker(driver, wait)

    # Locators
    APPLY_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Apply')]]")
    DOWNLOAD_BUTTONS = (By.XPATH, "//tbody//tr//td[not(contains(@class, 'collapse-cell'))]//button[contains(@class, 'rw-button--outlined')]//i[contains(@class, 'fa-download')]/..")
    CSV_DOWNLOAD_OPTION = (By.XPATH, "//ul[contains(@class, 'dropdown-menu') and contains(@style, 'display: block')]//a[.//label-details[contains(text(), 'csv')]]")
    
    @retry_on_exception()
    def set_date_range(self, start_date, end_date):
        """Set date range and click Apply button"""
        logger.info(f"Setting date range from {start_date} to {end_date}")
        self.date_picker.set_date_range(start_date, end_date)
        # Add sleep to ensure calendar is closed and Apply button is clickable
        self.click_element(self.APPLY_BUTTON, sleep_after=DEFAULT_SLEEP_TIME)
        logger.info("Date range applied")

    def has_no_results(self):
        no_results_locator = (By.XPATH, "//div[contains(@class, 'md-table-body') and not(contains(@class, 'ng-hide'))]//div[contains(@class, 'no-data')]")
        return self.is_element_present(no_results_locator)

    @retry_on_exception()
    def download_invoices(self):
        if self.has_no_results():
            logger.info("No results found - nothing to download")
            return False
        
        try:
            download_buttons = self.find_elements(self.DOWNLOAD_BUTTONS)
            logger.info(f"Found {len(download_buttons)} download buttons")
            
            for i, button in enumerate(download_buttons, 1):
                logger.info(f"Processing download button {i}")
                self.driver.execute_script("arguments[0].click();", button)
                self.click_element(self.CSV_DOWNLOAD_OPTION, sleep_after=1)
            
            return True
        except Exception as e:
            logger.error(f"Error during download process: {str(e)}")
            return False