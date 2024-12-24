import logging
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.retry import retry_on_exception
import time
logger = logging.getLogger(__name__)

class SideMenu(BasePage):
    # Sidebar Menu Locators
    SUMMARY_DASHBOARD_LINK = (By.CSS_SELECTOR, "a[href='#/dashboard']")
    SCRATCH_DASHBOARD_LINK = (By.CSS_SELECTOR, "a[href='#/dashboard-instant/']")
    REPORTS_LINK = (By.CSS_SELECTOR, "a[href='#/reports']")
    
    # Updated locators for retailer selection
    MORE_LOCATIONS_BUTTON = (By.XPATH, "//button[.//translate[text()='More locations']]")
    RETAILER_DROPDOWN_ITEMS = (
        By.XPATH,
        "//rw-list-item[not(@class='announcement-content__list-item') and not(@class='big-winners-list__item')]"
        "[.//rw-retailer-info]"
    )

    @retry_on_exception()
    def select_retailer(self, retailer_number):
        """
        Clicks the More locations button and selects the specified retailer from the dropdown
        
        Args:
            retailer_number (str): The retailer number to select (e.g. "176193")
        """
        logger.info(f"Selecting retailer number: {retailer_number}")
        
        # Click the More locations button to open dropdown
        self.click_element(self.MORE_LOCATIONS_BUTTON)
        time.sleep(1)
        
        # Find all retailer list items using base class method
        all_items = self.find_elements(self.RETAILER_DROPDOWN_ITEMS)
        logger.info(f"Found {len(all_items)} retailer list items:")
        
        for item in all_items:
            retailer_num = item.find_element(By.XPATH, ".//rw-retailer-id/span").text.strip()
            logger.info(f"Retailer number: {retailer_num}")
        # Find and click the matching retailer
        found_match = False
        for item in all_items:
            retailer_num = item.find_element(By.XPATH, ".//rw-retailer-id/span").text.strip()
            if retailer_num == retailer_number:
                logger.info(f"Found matching retailer {retailer_number}, clicking...")
                item.click()
                found_match = True
                time.sleep(3)
                break
        
        if not found_match:
            logger.error(f"No retailer found with number {retailer_number}")

    @retry_on_exception()
    def navigate_to_summary_dashboard(self):
        self.click_element(self.SUMMARY_DASHBOARD_LINK)

    @retry_on_exception()
    def navigate_to_scratch_dashboard(self):
        self.click_element(self.SCRATCH_DASHBOARD_LINK)

    @retry_on_exception()
    def navigate_to_reports(self):
        self.click_element(self.REPORTS_LINK) 