from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .components.side_menu import SideMenu
from utils.date_picker import DatePicker
import time

class ReportsPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.side_menu = SideMenu(driver, wait)
        self.date_picker = DatePicker(driver, wait, {
            'from_date': 'from-date',  # Using the specific ID for from-date
            'to_date': 'to-date'       # Using the specific ID for to-date
        })

    # Locators
    SEARCH_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Search')]]")

    def set_date_range(self, start_date, end_date):
        """
        Set the date range for reports using the calendar picker.
        
        Args:
            start_date (str or datetime): Start date in 'MM/DD/YYYY' format or datetime object
            end_date (str or datetime): End date in 'MM/DD/YYYY' format or datetime object
        """
        self.date_picker.set_date_range(start_date, end_date)
        # Click Search button
        search_button = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", search_button)
