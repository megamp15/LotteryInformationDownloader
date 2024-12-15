from utils.webdriver_setup import WebDriverSetup
from pages.login_page import LoginPage
from pages.summary_dashboard_page import SummaryDashboardPage
from pages.invoice_details_page import InvoiceDetailsPage
from pages.scratch_dashboard_page import ScratchDashboardPage
from pages.liabilities_details_page import LiabilitiesDetailsPage
from pages.reports_page import ReportsPage
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
        liabilities_details = LiabilitiesDetailsPage(driver, wait)
        reports_page = ReportsPage(driver, wait)
        side_menu = SideMenu(driver, wait)

        # Login workflow - Goes to summary dashboard by default
        login_page.navigate_to()
        login_page.login("mpkasar@gmail.com", "TX786110.")
        time.sleep(2)

        # Navigate to Invoice Details from summary dashboard
        summary_dashboard.click_invoice_details()
        time.sleep(2)
        invoice_details.set_date_range("11/01/2024", "11/30/2024")
        time.sleep(2)
        invoice_details.download_invoices()

        # Navigate to Scratch Dashboard and then Liabilities
        side_menu.navigate_to_scratch_dashboard()
        scratch_dashboard.click_liabilities_details()
        liabilities_details.set_date_range("11/01/2024", "11/30/2024")
        time.sleep(2)
        liabilities_details.download_xlsx()
        time.sleep(2)

        # Navigate to Reports Dashboard
        side_menu.navigate_to_reports()
        reports_page.select_report("Pack Inventory")
        reports_page.set_date_range("11/01/2024", "11/30/2024")
        time.sleep(2)
        reports_page.click_search()
        time.sleep(2)
        reports_page.download_reports()

        reports_page.select_report("Packs Activated")
        time.sleep(2)
        reports_page.click_search()
        time.sleep(2)
        reports_page.download_reports()

        reports_page.select_report("Full Statement")
        time.sleep(2)
        reports_page.click_search()
        time.sleep(2)
        reports_page.download_reports()

        # Keep browser open for debugging
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
