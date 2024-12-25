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

class RetailerInfo:
    def __init__(self, retailer_number, company_name):
        self.retailer_number = retailer_number
        self.company_name = company_name

class DataExtractor:
    def __init__(self, driver, wait, mode='--script'):
        self.driver = driver
        self.wait = wait
        self.mode = mode
        self.initialize_pages()
        self.report_processor = ReportProcessor()
        self.retailers = []  # List to store RetailerInfo objects

    def initialize_pages(self):
        """Initialize all page objects"""
        self.login_page = LoginPage(self.driver, self.wait)
        self.summary_dashboard = SummaryDashboardPage(self.driver, self.wait)
        self.invoice_details = InvoiceDetailsPage(self.driver, self.wait)
        self.scratch_dashboard = ScratchDashboardPage(self.driver, self.wait)
        self.liabilities_details = LiabilitiesDetailsPage(self.driver, self.wait)
        self.reports_page = ReportsPage(self.driver, self.wait)
        self.side_menu = SideMenu(self.driver, self.wait)

    def add_retailer(self, retailer_number, company_name):
        """Add a retailer to be processed"""
        self.retailers.append(RetailerInfo(retailer_number, company_name))

    def process_all_retailers(self):
        """Process data for all retailers"""
        logger.info("Starting to process all retailers")
        
        # Login only once
        self.login_page.navigate_to()
        self.login_page.login(LOGIN_EMAIL, LOGIN_PASSWORD)
        
        for retailer in self.retailers:
            logger.info(f"Processing retailer {retailer.retailer_number} for {retailer.company_name}")
            
            # Select the retailer
            self.side_menu.select_retailer(retailer.retailer_number)
            time.sleep(1)  # Wait for retailer selection to take effect
            
        # Extract data for this retailer
            self.extract_invoice_data()
            self.extract_liabilities_data()
            self.extract_reports_data()
            self.process_downloaded_data()

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
        try:
            logger.info("Extracting reports data...")
            self.side_menu.navigate_to_reports()
            
            self.reports_page.set_date_range(DEFAULT_START_DATE, DEFAULT_END_DATE)
            
            for report_type in REPORT_TYPES.values():
                try:
                    logger.info(f"Downloading report: {report_type}")
                    self.reports_page.select_report(report_type)                    
                    self.reports_page.click_search()                    
                    if not self.reports_page.download_reports():
                        logger.error(f"Failed to download report: {report_type}, continuing to next report...")
                    
                except Exception as e:
                    logger.error(f"Error downloading report {report_type}: {str(e)}")
                    logger.error("Continuing to next report...")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in extract_reports_data: {str(e)}")
            logger.error("Continuing with next retailer...")

    def process_downloaded_data(self):
        """Process all downloaded data"""
        logger.info("Processing downloaded data...")
        # self.report_processor.process_all_reports() 