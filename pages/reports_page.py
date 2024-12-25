from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.retry import retry_on_exception
from utils.date_picker import DatePicker
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
from config.settings import DEFAULT_SLEEP_TIME

logger = logging.getLogger(__name__)

class ReportsPage(BasePage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)
        self.date_picker = DatePicker(driver, wait, {
            'from_date': 'from-date',
            'to_date': 'to-date'
        })

    # Locators
    SEARCH_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Search')]]")
    REPORT_NAME_DROPDOWN = (By.ID, "raportName")
    REPORT_OPTION = (By.XPATH, "//md-option//div[contains(text(), '{}')]")
    TABLE_ROWS = (By.CSS_SELECTOR, "tr.md-table-row")
    REPORT_NAME_LINKS = (By.XPATH, "//td[contains(@class, 'md-table-cell')]//dropdown//span[@ng-transclude='dropdownToggle']//a[not(@ng-click)]")
    CSV_DOWNLOAD_OPTION = (By.XPATH, "//ul[contains(@class, 'dropdown-menu') and contains(@style, 'display: block')]//a[.//label-details[contains(text(), 'csv')]]")

    @retry_on_exception()
    def click_search(self):
        self.click_element(self.SEARCH_BUTTON)
        time.sleep(DEFAULT_SLEEP_TIME)

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
    def select_report(self, report_name):
        logger.info(f"Selecting report: {report_name}")
        self.click_element(self.REPORT_NAME_DROPDOWN)
        report_option = (By.XPATH, self.REPORT_OPTION[1].format(report_name))
        self.find_element(report_option)  # Wait for option to be present
        self.click_element(report_option)
        logger.info(f"Selected report: {report_name}")

    def set_date_range(self, start_date, end_date):
        logger.info(f"Setting date range from {start_date} to {end_date}")
        self.date_picker.set_date_range(start_date, end_date)
        logger.info("Date range set")

    @retry_on_exception()
    def download_reports(self):
        """Download reports if available"""
        if self.has_no_results():
            logger.info("No results found - nothing to download")
            return False
        
        try:
            logger.info("Starting reports download...")
            report_links = self.find_elements(self.REPORT_NAME_LINKS)
            logger.info(f"Found {len(report_links)} reports to download")
            
            if not report_links:
                return False
            
            for i, link in enumerate(report_links, 1):
                self.driver.execute_script("arguments[0].click();", link)
                self.click_element(self.CSV_DOWNLOAD_OPTION, sleep_after=1)
            
            return True
        except Exception as e:
            logger.error(f"Error downloading reports: {str(e)}")
            return False
