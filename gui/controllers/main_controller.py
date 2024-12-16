import logging
from threading import Thread
from ..models.settings_model import SettingsModel
from config.settings import *
from core.data_extractor import browser_session, DataExtractor

logger = logging.getLogger(__name__)

class MainController:
    def __init__(self):
        self.settings = SettingsModel()
        self.current_thread = None
        self.stop_requested = False

    def on_excel_selected(self, filename):
        self.settings.excel_file = filename
        logger.info(f"Excel file selected: {filename}")

    def on_dir_selected(self, dirname):
        self.settings.download_dir = dirname
        logger.info(f"Download directory selected: {dirname}")

    def start_download(self, excel_path, download_dir, start_date, end_date):
        if self.current_thread and self.current_thread.is_alive():
            logger.warning("Download already in progress")
            return

        self.stop_requested = False
        self.current_thread = Thread(
            target=self._download_process,
            args=(excel_path, download_dir, start_date, end_date)
        )
        self.current_thread.start()

    def stop_download(self):
        self.stop_requested = True
        logger.info("Stopping download process...")

    def _download_process(self, excel_path, download_dir, start_date, end_date):
        try:
            with browser_session() as (driver, wait):
                extractor = DataExtractor(driver, wait)
                extractor.login_page.navigate_to()
                extractor.login_page.login(LOGIN_EMAIL, LOGIN_PASSWORD)
                
                if not self.stop_requested:
                    extractor.extract_invoice_data()
                if not self.stop_requested:
                    extractor.extract_liabilities_data()
                if not self.stop_requested:
                    extractor.extract_reports_data()
                if not self.stop_requested:
                    extractor.process_downloaded_data()
                
                logger.info("Download process completed successfully")
        except Exception as e:
            logger.error(f"Error during download: {str(e)}") 