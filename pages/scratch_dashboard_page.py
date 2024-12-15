from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .components.side_menu import SideMenu
import time
class ScratchDashboardPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.side_menu = SideMenu(driver, wait)

    # Locators
    LIABILITIES_DETAILS_LINK = (By.XPATH, "//a[contains(@ui-sref, 'manageInventory-listByType') and contains(@href, 'tabId=liability')]")
    HISTORY_BUTTON = (By.XPATH, "//button[.//translate[text()='History']]")
    def click_liabilities_details(self):
        liabilities_details_link = self.wait.until(
            EC.element_to_be_clickable(self.LIABILITIES_DETAILS_LINK)
        )
        self.driver.execute_script("arguments[0].click();", liabilities_details_link)

        history_button = self.wait.until(
            EC.element_to_be_clickable(self.HISTORY_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", history_button)
        time.sleep(2)

