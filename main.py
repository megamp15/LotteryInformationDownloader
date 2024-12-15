from utils.webdriver_setup import WebDriverSetup
from pages.login_page import LoginPage
from pages.summary_dashboard_page import SummaryDashboardPage
from pages.invoice_details_page import InvoiceDetailsPage
from pages.scratch_dashboard_page import ScratchDashboardPage
from pages.components.side_menu import SideMenu
from datetime import datetime, timedelta
import time

def main():
    driver, wait = WebDriverSetup.get_driver()

    try:
        # Initialize pages and components
        login_page = LoginPage(driver, wait)
        summary_dashboard = SummaryDashboardPage(driver, wait)
        invoice_details = InvoiceDetailsPage(driver, wait)
        scratch_dashboard = ScratchDashboardPage(driver, wait)
        side_menu = SideMenu(driver, wait)

        # Login workflow - Goes to summary dashboard by default
        login_page.navigate_to()
        login_page.login("mpkasar@gmail.com", "TX786110.")
        time.sleep(2)
        # Navigate to Invoice Details from summary dashboard
        summary_dashboard.click_invoice_details()
        time.sleep(2)
        # Set date range (example: last 30 days)
        # end_date = datetime.now()
        # start_date = end_date - timedelta(days=30)
        invoice_details.set_date_range("11/06/2024", "12/01/2024")
        time.sleep(2)
        invoice_details.download_invoices()

        # Keep browser open for debugging
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
