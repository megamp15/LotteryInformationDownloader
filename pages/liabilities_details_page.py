from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.retry import retry_on_exception
from utils.date_picker import DatePicker
import logging

logger = logging.getLogger(__name__)

class LiabilitiesDetailsPage(BasePage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait)
        self.date_picker = DatePicker(driver, wait, {
            'from_date': 'date-from',
            'to_date': 'date-to'
        })

    # Locators
    SEARCH_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Search')]]")
    ACTIONS_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Actions')]]")
    XLSX_DOWNLOAD_OPTION = (By.XPATH, "//a[@ng-click and .//label-details[contains(text(), '.xlsx')]]")

    @retry_on_exception()
    def set_date_range(self, start_date, end_date):
        self.date_picker.set_date_range(start_date, end_date)
        self.click_element(self.SEARCH_BUTTON)

    @retry_on_exception()
    def download_xlsx(self):
        try:
            self.click_element(self.ACTIONS_BUTTON, sleep_after=1)
            self.click_element(self.XLSX_DOWNLOAD_OPTION, sleep_after=1)
            return True
        except Exception as e:
            logger.error(f"Error during XLSX download: {str(e)}")
            return False
