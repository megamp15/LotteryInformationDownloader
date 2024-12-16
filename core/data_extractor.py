import logging
import time
from contextlib import contextmanager
from utils.webdriver_setup import WebDriverSetup
from config.settings import *
from pages.login_page import LoginPage
from pages.summary_dashboard_page import SummaryDashboardPage
from pages.invoice_details_page import InvoiceDetailsPage
from pages.scratch_dashboard_page import ScratchDashboardPage
from pages.liabilities_details_page import LiabilitiesDetailsPage
from pages.reports_page import ReportsPage
from pages.components.side_menu import SideMenu
from data_processors.report_processor import ReportProcessor

logger = logging.getLogger(__name__)

@contextmanager
def browser_session():
    driver, wait = WebDriverSetup.get_driver()
    try:
        yield driver, wait
    except Exception as e:
        logger.error(f"Browser session error: {e}")
        raise
    finally:
        driver.quit()

class DataExtractor:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.initialize_pages()
        self.report_processor = ReportProcessor()

    def initialize_pages(self):
        """Initialize all page objects"""
        self.login_page = LoginPage(self.driver, self.wait)
        self.summary_dashboard = SummaryDashboardPage(self.driver, self.wait)
        self.invoice_details = InvoiceDetailsPage(self.driver, self.wait)
        self.scratch_dashboard = ScratchDashboardPage(self.driver, self.wait)
        self.liabilities_details = LiabilitiesDetailsPage(self.driver, self.wait)
        self.reports_page = ReportsPage(self.driver, self.wait)
        self.side_menu = SideMenu(self.driver, self.wait)

    def extract_invoice_data(self):
        """Extract invoice related data"""
        logger.info("Extracting invoice data...")
        self.summary_dashboard.click_invoice_details()
        self.invoice_details.set_date_range(DEFAULT_START_DATE, DEFAULT_END_DATE)
        self.invoice_details.download_invoices()

    def extract_liabilities_data(self):
        """Extract liabilities related data"""
        logger.info("Extracting liabilities data...")
        self.side_menu.navigate_to_scratch_dashboard()
        self.scratch_dashboard.click_liabilities_details()
        self.liabilities_details.set_date_range(DEFAULT_START_DATE, DEFAULT_END_DATE)
        self.liabilities_details.download_xlsx()

    def extract_reports_data(self):
        """Extract reports data"""
        logger.info("Extracting reports data...")
        self.side_menu.navigate_to_reports()
        time.sleep(DEFAULT_SLEEP_TIME * 2)
        
        self.reports_page.set_date_range(DEFAULT_START_DATE, DEFAULT_END_DATE)
        time.sleep(DEFAULT_SLEEP_TIME * 2)
        
        for report_type in REPORT_TYPES.values():
            logger.info(f"Downloading report: {report_type}")
            self.reports_page.select_report(report_type)
            time.sleep(DEFAULT_SLEEP_TIME * 2)
            
            self.reports_page.click_search()
            time.sleep(DEFAULT_SLEEP_TIME * 3)
            
            if not self.reports_page.download_reports():
                logger.warning(f"Failed to download report: {report_type}")
            
            time.sleep(DEFAULT_SLEEP_TIME * 3)

    def process_downloaded_data(self):
        """Process all downloaded data"""
        logger.info("Processing downloaded data...")
        # self.report_processor.process_all_reports() 