from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.retry import retry_on_exception

class SummaryDashboardPage(BasePage):
    # Locators
    INVOICE_DETAILS_LINK = (By.XPATH, "//a[.//translate[text()='Invoice Details']]")

    @retry_on_exception()
    def click_invoice_details(self):
        self.click_element(self.INVOICE_DETAILS_LINK)
