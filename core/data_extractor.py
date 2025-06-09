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
from data_processors.liability_processor import LiabilityProcessor

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
    def __init__(self, driver, wait, mode='--script', company_name=None, download_path=None, start_date=None, end_date=None):
        self.driver = driver
        self.wait = wait
        self.mode = mode
        self.company_name = company_name
        self.download_path = download_path
        self.start_date = start_date or DEFAULT_START_DATE
        self.end_date = end_date or DEFAULT_END_DATE
        self.retailer_number = None

        # Initialize pages
        self.login_page = LoginPage(driver, wait)
        self.summary_dashboard = SummaryDashboardPage(driver, wait)
        self.invoice_details = InvoiceDetailsPage(driver, wait)
        self.scratch_dashboard = ScratchDashboardPage(driver, wait)
        self.liabilities_details = LiabilitiesDetailsPage(driver, wait)
        self.reports_page = ReportsPage(driver, wait)
        self.side_menu = SideMenu(driver, wait)

    def add_retailer(self, retailer_number, company_name):
        """Add retailer info for script mode"""
        self.retailer_number = retailer_number
        self.company_name = company_name

    def process_all_retailers(self):
        """Process data for all retailers"""
        logger.info("Starting to process all retailers")
        
        # Login is now handled before calling this method
        logger.info(f"Processing retailer {self.retailer_number} for {self.company_name}")
        
        # Select the retailer
        self.side_menu.select_retailer(self.retailer_number)
        time.sleep(1)  # Wait for retailer selection to take effect
        
        # # Extract data for this retailer
        # self.extract_invoice_data()
        # self.extract_liabilities_data()
        # self.extract_reports_data()
        self.process_downloaded_data()

    def extract_invoice_data(self):
        """Extract invoice related data"""
        logger.info("Extracting invoice data...")
        self.summary_dashboard.click_invoice_details()
        self.invoice_details.set_date_range(self.start_date, self.end_date)
        self.invoice_details.download_invoices()

    # def extract_liabilities_data(self):
    #     """Extract liabilities related data"""
    #     try:
    #         logger.info("Extracting liabilities data...")
            
    #         # Get current retailer info if not set (GUI mode)
    #         if not self.company_name:
    #             current_retailer = self.side_menu.get_current_retailer()
    #             if current_retailer:
    #                 self.company_name = current_retailer
    #             else:
    #                 logger.error("No retailer selected")
    #                 return
            
    #         self.side_menu.navigate_to_scratch_dashboard()
    #         self.scratch_dashboard.click_liabilities_details()
    #         self.liabilities_details.set_date_range(self.start_date, self.end_date)
    #         self.liabilities_details.download_xlsx()
            
    #     except Exception as e:
    #         logger.error(f"Error extracting liabilities data: {str(e)}")

    def extract_reports_data(self):
        """Extract reports data"""
        try:
            logger.info("Extracting reports data...")
            self.side_menu.navigate_to_reports()
            
            self.reports_page.set_date_range(self.start_date, self.end_date)
            
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
        try:
            if not self.company_name:
                logger.error("No company name provided for processing")
                return

            logger.info(f"Processing data for company: {self.company_name}")
                
            # # Process liability data first
            # liability_processor = LiabilityProcessor(self.download_path, self.company_name, self.start_date, self.end_date)
            # liability_processor.process_liability_data()
            
            # Then process any remaining reports
            report_processor = ReportProcessor(self.download_path, self.company_name, self.start_date, self.end_date)
            report_processor.process_report_data()
            
        except Exception as e:
            logger.error(f"Error processing downloaded data: {str(e)}") 