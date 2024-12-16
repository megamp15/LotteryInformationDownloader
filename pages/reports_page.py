from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.retry import retry_on_exception
from utils.date_picker import DatePicker
from config.settings import DEFAULT_SLEEP_TIME
import logging
import time

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
    NO_RESULTS_MESSAGE = (By.XPATH, "//div[contains(@class, 'md-table-body') and not(contains(@class, 'ng-hide'))]//div[contains(text(), 'Sorry, no results were found.')]")
    REPORT_NAME_LINKS = (By.XPATH, "//td[contains(@class, 'md-table-cell')]//dropdown//span[@ng-transclude='dropdownToggle']//a[not(@ng-click)]")
    CSV_DOWNLOAD_OPTION = (By.XPATH, "//ul[contains(@class, 'dropdown-menu') and contains(@style, 'display: block')]//a[.//label-details[contains(text(), 'csv')]]")

    @retry_on_exception()
    def click_search(self):
        self.click_element(self.SEARCH_BUTTON)
        time.sleep(DEFAULT_SLEEP_TIME)

    def has_no_results(self):
        return self.is_element_present(self.NO_RESULTS_MESSAGE)

    @retry_on_exception()
    def select_report(self, report_name):
        self.click_element(self.REPORT_NAME_DROPDOWN)
        time.sleep(DEFAULT_SLEEP_TIME)        
        report_option = (By.XPATH, self.REPORT_OPTION[1].format(report_name))
        self.click_element(report_option)
        time.sleep(DEFAULT_SLEEP_TIME)
    def set_date_range(self, start_date, end_date):
        self.date_picker.set_date_range(start_date, end_date)
        time.sleep(DEFAULT_SLEEP_TIME)
    @retry_on_exception()
    def download_reports(self):
        time.sleep(DEFAULT_SLEEP_TIME)
        
        if self.has_no_results():
            logger.info("No results found - nothing to download")
            return False
        
        try:
            report_links = self.find_elements(self.REPORT_NAME_LINKS)
            
            if not report_links:
                logger.info("No report links found")
                return False
                
            for link in report_links:
                self.driver.execute_script("arguments[0].click();", link)
                time.sleep(1)
                self.click_element(self.CSV_DOWNLOAD_OPTION)
                time.sleep(2)
            
            return True
        except Exception as e:
            logger.error(f"Error during download process: {str(e)}")
            return False
