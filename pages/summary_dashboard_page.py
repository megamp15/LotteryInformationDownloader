from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .components.side_menu import SideMenu

class SummaryDashboardPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.side_menu = SideMenu(driver, wait)

    # Locators
    INVOICE_DETAILS_LINK = (By.XPATH, "//a[.//translate[text()='Invoice Details']]")

    def click_invoice_details(self):
        invoice_details_link = self.wait.until(
            EC.element_to_be_clickable(self.INVOICE_DETAILS_LINK)
        )
        self.driver.execute_script("arguments[0].click();", invoice_details_link)
