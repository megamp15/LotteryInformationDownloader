from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .components.side_menu import SideMenu
from utils.date_picker import DatePicker
import time

class LiabilitiesDetailsPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.side_menu = SideMenu(driver, wait)
        self.date_picker = DatePicker(driver, wait, {
            'from_date': 'date-from',
            'to_date': 'date-to'
        })

    # Locators
    SEARCH_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Search')]]")
    ACTIONS_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Actions')]]")
    XLSX_DOWNLOAD_OPTION = (By.XPATH, "//a[@ng-click and .//label-details[contains(text(), '.xlsx')]]")

    def set_date_range(self, start_date, end_date):
        """
        Set the date range for invoice details using the calendar picker.
        
        Args:
            start_date (str or datetime): Start date in 'MM/DD/YYYY' format or datetime object
            end_date (str or datetime): End date in 'MM/DD/YYYY' format or datetime object
        """
        self.date_picker.set_date_range(start_date, end_date)
        search_button = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", search_button)

    def download_xlsx(self):
        """Click the Actions button and select the XLSX download option"""
        try:
            actions_button = self.wait.until(
                EC.element_to_be_clickable(self.ACTIONS_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", actions_button)
            time.sleep(1)

            xlsx_download_option = self.wait.until(
                EC.element_to_be_clickable(self.XLSX_DOWNLOAD_OPTION)
            )
            self.driver.execute_script("arguments[0].click();", xlsx_download_option)
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error during XLSX download: {str(e)}")
            return False
