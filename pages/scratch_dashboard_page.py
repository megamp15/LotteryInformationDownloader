from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.retry import retry_on_exception

class ScratchDashboardPage(BasePage):
    # Locators
    LIABILITIES_DETAILS_LINK = (By.XPATH, "//a[contains(@ui-sref, 'manageInventory-listByType') and contains(@href, 'tabId=liability')]")
    HISTORY_BUTTON = (By.XPATH, "//button[.//translate[text()='History']]")

    @retry_on_exception()
    def click_liabilities_details(self):
        self.click_element(self.LIABILITIES_DETAILS_LINK)
        self.click_element(self.HISTORY_BUTTON, sleep_after=2)
