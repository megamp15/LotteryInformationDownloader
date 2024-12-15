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
            'from_date': 'from-date',
            'to_date': 'to-date'
        })

    # Locators
    SEARCH_BUTTON = (By.XPATH, "//button[.//ng-transclude[contains(text(), 'Search')]]")
    REPORT_NAME_DROPDOWN = (By.ID, "raportName")
    REPORT_OPTION = (By.XPATH, "//md-option//div[contains(text(), '{}')]")
    NO_RESULTS_MESSAGE = (By.XPATH, "//div[contains(text(), 'Sorry, no results were found.')]")
    
    # Report download related locators
    REPORT_NAME_LINKS = (By.XPATH, "//td[not(contains(@class, 'collapse-cell'))]//dropdown//a[not(contains(@class, 'dropdown-toggle'))]")
    CSV_DOWNLOAD_OPTION = (By.XPATH, "//ul[contains(@class, 'dropdown-menu')]//a[.//label-details[contains(text(), 'csv')]]")

    def click_search(self):
        """Click the Search button"""
        search_button = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", search_button)

    def has_no_results(self):
        """
        Check if the 'no results' message is displayed.
        
        Returns:
            bool: True if no results are found, False otherwise
        """
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.NO_RESULTS_MESSAGE)
            )
            return True
        except:
            return False

    def select_report(self, report_name):
        """
        Select a report from the dropdown menu.
        
        Args:
            report_name (str): Name of the report to select (e.g., 'Pack Inventory')
        """
        # Click the dropdown to open it
        report_dropdown = self.wait.until(
            EC.element_to_be_clickable(self.REPORT_NAME_DROPDOWN)
        )
        self.driver.execute_script("arguments[0].click();", report_dropdown)
        time.sleep(1)  # Wait for dropdown to open

        # Select the specific report
        report_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, self.REPORT_OPTION[1].format(report_name))
            )
        )
        self.driver.execute_script("arguments[0].click();", report_option)
        time.sleep(1)  # Wait for selection to register

    def set_date_range(self, start_date, end_date):
        """
        Set the date range for reports using the calendar picker.
        
        Args:
            start_date (str or datetime): Start date in 'MM/DD/YYYY' format or datetime object
            end_date (str or datetime): End date in 'MM/DD/YYYY' format or datetime object
        """
        self.date_picker.set_date_range(start_date, end_date)

    def download_reports(self):
        """Download CSV for all available reports in the results"""
        if self.has_no_results():
            print("No results found - nothing to download")
            return False

        try:
            # Find all report name links
            report_links = self.wait.until(
                EC.presence_of_all_elements_located(self.REPORT_NAME_LINKS)
            )
            
            print(f"Found {len(report_links)} reports to download")
            
            for i, link in enumerate(report_links, 1):
                print(f"\nProcessing report {i}")
                self.driver.execute_script("arguments[0].click();", link)
                
                # Wait for and click CSV option
                csv_option = self.wait.until(
                    EC.element_to_be_clickable(self.CSV_DOWNLOAD_OPTION)
                )
                print(f"CSV option found: {csv_option.get_attribute('outerHTML')}")
                self.driver.execute_script("arguments[0].click();", csv_option)
                time.sleep(1)  # Wait between downloads
            
            return True
        except Exception as e:
            print(f"Error during download process: {str(e)}")
            return False
