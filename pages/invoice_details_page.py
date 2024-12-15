from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .components.side_menu import SideMenu
from datetime import datetime
import time
from utils.date_picker import DatePicker

class InvoiceDetailsPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.side_menu = SideMenu(driver, wait)
        self.date_picker = DatePicker(driver, wait)

    # Locators
    APPLY_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Apply')]]")

    # Download related locators
    DOWNLOAD_BUTTONS = (By.XPATH, "//tbody//tr//td[not(contains(@class, 'collapse-cell'))]//button[contains(@class, 'rw-button--outlined')]//i[contains(@class, 'fa-download')]/..")
    CSV_DOWNLOAD_OPTION = (By.XPATH, "//ul[contains(@class, 'dropdown-menu') and contains(@style, 'display: block')]//a[.//label-details[contains(text(), 'csv')]]")
    
    def set_date_range(self, start_date, end_date):
        """
        Set the date range for invoice details using the calendar picker.
        
        Args:
            start_date (str or datetime): Start date in 'MM/DD/YYYY' format or datetime object
            end_date (str or datetime): End date in 'MM/DD/YYYY' format or datetime object
        """
        self.date_picker.set_date_range(start_date, end_date)
        # Click Apply button
        apply_button = self.wait.until(
            EC.element_to_be_clickable(self.APPLY_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", apply_button)


    def has_no_results(self):
        """
        Check if the 'no results' message is displayed.
        
        Returns:
            bool: True if no results are found, False otherwise
        """
        try:
            # Look for the 'no results' div without ng-hide class
            no_results_locator = (By.XPATH, "//div[contains(@class, 'md-table-body') and not(contains(@class, 'ng-hide'))]//div[contains(@class, 'no-data')]")
            
            # Wait a short time for the element to be visible
            no_results_element = self.wait.until(
                EC.visibility_of_element_located(no_results_locator)
            )
            return "Sorry, no results were found." in no_results_element.text
        except:
            return False

    def download_invoices(self):
        """Click download button for each invoice row and select CSV option"""
        # First check if there are no results
        if self.has_no_results():
            print("No results found - nothing to download")
            return False
        
        try:
            # Find all download buttons in the table
            download_buttons = self.wait.until(
                EC.presence_of_all_elements_located(self.DOWNLOAD_BUTTONS)
            )
            
            print(f"Found {len(download_buttons)} download buttons")
            
            for i, button in enumerate(download_buttons, 1):
                print(f"\nProcessing download button {i}")
                self.driver.execute_script("arguments[0].click();", button)
            
            #     # Wait for and click CSV option
                csv_option = self.wait.until(
                    EC.element_to_be_clickable(self.CSV_DOWNLOAD_OPTION)
                )
                self.driver.execute_script("arguments[0].click();", csv_option)
                time.sleep(1)  # Wait between rows
            
            return True
        except Exception as e:
            print(f"Error during download process: {str(e)}")
            return False