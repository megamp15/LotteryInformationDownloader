import logging
from threading import Thread
from ..models.settings_model import SettingsModel
from config.settings import *
from core.data_extractor import browser_session, DataExtractor
import pandas as pd
from utils.webdriver_setup import WebDriverSetup
import time
import os
from tkinter import messagebox

logger = logging.getLogger(__name__)

class GUILogHandler(logging.Handler):
    def __init__(self, status_callback):
        super().__init__()
        self.status_callback = status_callback

    def emit(self, record):
        msg = self.format(record)
        self.status_callback(msg)

class MainController:
    def __init__(self, root=None):
        self.settings = SettingsModel()
        self.current_thread = None
        self.stop_requested = False
        self.gui_handler = None
        self.root = root

    def set_status_callback(self, callback):
        """Set up logging to GUI"""
        self.gui_handler = GUILogHandler(callback)
        self.gui_handler.setFormatter(
            logging.Formatter('%(levelname)s - %(message)s')
        )
        
        # Get the root logger to capture all messages
        root_logger = logging.getLogger()
        root_logger.addHandler(self.gui_handler)
        
        # Optionally set level to ensure we capture all messages
        root_logger.setLevel(logging.INFO)

    def on_excel_selected(self, filename):
        self.settings.excel_file = filename
        logger.info(f"Excel file selected: {filename}")

    def on_dir_selected(self, dirname):
        self.settings.download_dir = dirname
        logger.info(f"Download directory selected: {dirname}")

    def start_download(self, excel_path, download_dir, start_date, end_date, delete_files=False):
        if self.current_thread and self.current_thread.is_alive():
            logger.warning("Download already in progress")
            return

        self.stop_requested = False
        self.current_thread = Thread(
            target=self._download_process,
            args=(excel_path, download_dir, start_date, end_date, delete_files)
        )
        self.current_thread.start()

    def stop_download(self):
        self.stop_requested = True
        logger.info("Stopping download process...")

    def delete_files(self, download_dir, df, single_retailer=""):
        """Delete files in retailer folders"""
        try:
            if single_retailer:
                # Delete files for single retailer
                del_file_dir = os.path.join(download_dir, single_retailer.strip())
                if os.path.exists(del_file_dir):
                    del_file_list = os.listdir(del_file_dir)
                    for f in del_file_list:
                        os.remove(os.path.join(del_file_dir, f))
                    logger.info(f"Deleted files for {single_retailer}")
            else:
                # Delete files for all retailers
                for retailer in df['COMPANY']:
                    del_file_dir = os.path.join(download_dir, retailer.strip())
                    if os.path.exists(del_file_dir):
                        del_file_list = os.listdir(del_file_dir)
                        for f in del_file_list:
                            os.remove(os.path.join(del_file_dir, f))
                logger.info("Deleted files for all retailers")
        except Exception as e:
            logger.error(f"Error deleting files: {str(e)}")

    def _download_process(self, excel_path, download_dir, start_date, end_date, delete_files=False):
        try:
            logger.info(f"Reading Excel file: {excel_path}")
            df = pd.read_excel(excel_path)
            logger.info(f"Found {len(df)} retailers to process")

            # Delete existing files if requested
            if delete_files:
                self.delete_files(download_dir, df)

            for index, row in df.iterrows():
                if self.stop_requested:
                    logger.info("Stop requested, breaking loop")
                    break

                company_name = row['COMPANY'].strip()
                username = row['USERNAME'].strip()
                retailer_number = str(row['RETAILER NUMBER']).strip()

                logger.info(f"\nProcessing retailer: {company_name}")
                
                try:
                    driver, wait = WebDriverSetup.get_driver(
                        mode='--gui',
                        company_name=company_name,
                        download_path=download_dir
                    )
                    
                    extractor = DataExtractor(driver, wait, mode='--gui')
                    extractor.login_page.navigate_to()
                    extractor.login_page.login(username, row['PASSWORD'].strip())
                    
                    logger.info(f"Selecting retailer {retailer_number}")
                    extractor.side_menu.select_retailer(retailer_number)
                    time.sleep(2)
                    
                    if not self.stop_requested:
                        extractor.extract_invoice_data()
                    if not self.stop_requested:
                        extractor.extract_liabilities_data()
                    if not self.stop_requested:
                        extractor.extract_reports_data()
                    if not self.stop_requested:
                        extractor.process_downloaded_data()
                    
                    logger.info(f"Completed processing {company_name}")
                    
                except Exception as e:
                    logger.error(f"Error processing {company_name}: {str(e)}")
                    continue
                finally:
                    driver.quit()
                    time.sleep(2)
                    
            logger.info("All retailers processed successfully")
            
        except Exception as e:
            logger.error(f"Error during download process: {str(e)}")

    def create_template(self, save_path):
        """Create and save template Excel file"""
        data = {
            'USERNAME': ['example@email.com'],
            'PASSWORD': ['password123'],
            'RETAILER NUMBER': ['123456'],
            'COMPANY': ['COMPANY_NAME']
        }
        
        df = pd.DataFrame(data)
        df.to_excel(save_path, index=False)
        logger.info(f"Template Excel file created at: {save_path}")