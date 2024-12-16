from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.retry import retry_on_exception

class SideMenu(BasePage):
    # Sidebar Menu Locators
    SUMMARY_DASHBOARD_LINK = (By.CSS_SELECTOR, "a[href='#/dashboard']")
    SCRATCH_DASHBOARD_LINK = (By.CSS_SELECTOR, "a[href='#/dashboard-instant/']")
    REPORTS_LINK = (By.CSS_SELECTOR, "a[href='#/reports']")

    @retry_on_exception()
    def navigate_to_summary_dashboard(self):
        self.click_element(self.SUMMARY_DASHBOARD_LINK)

    @retry_on_exception()
    def navigate_to_scratch_dashboard(self):
        self.click_element(self.SCRATCH_DASHBOARD_LINK)

    @retry_on_exception()
    def navigate_to_reports(self):
        self.click_element(self.REPORTS_LINK) 