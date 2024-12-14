from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SideMenu:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # Sidebar Menu Locators
    SUMMARY_DASHBOARD_LINK = (By.CSS_SELECTOR, "a[href='#/dashboard']")
    SCRATCH_DASHBOARD_LINK = (By.CSS_SELECTOR, "a[href='#/dashboard-instant/']")
    REPORTS_LINK = (By.CSS_SELECTOR, "a[href='#/reports']")

    def navigate_to_summary_dashboard(self):
        link = self.wait.until(EC.element_to_be_clickable(self.SUMMARY_DASHBOARD_LINK))
        self.driver.execute_script("arguments[0].click();", link)

    def navigate_to_scratch_dashboard(self):
        link = self.wait.until(EC.element_to_be_clickable(self.SCRATCH_DASHBOARD_LINK))
        self.driver.execute_script("arguments[0].click();", link)

    def navigate_to_reports(self):
        link = self.wait.until(EC.element_to_be_clickable(self.REPORTS_LINK))
        self.driver.execute_script("arguments[0].click();", link) 