import tkinter as tk
import argparse
import logging
from gui.views.main_window import MainWindow
from gui.controllers.main_controller import MainController
from core.data_extractor import DataExtractor, browser_session
from config.settings import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_script_mode():
    """Run in script mode (no GUI)"""
    with browser_session() as (driver, wait):
        extractor = DataExtractor(driver, wait)
        
        # Login and extract data
        extractor.login_page.navigate_to()
        extractor.login_page.login(LOGIN_EMAIL, LOGIN_PASSWORD)
        extractor.side_menu.select_retailer(RETAILER_NUM)
        
        extractor.extract_invoice_data()
        extractor.extract_liabilities_data()
        extractor.extract_reports_data()
        
        # Process downloaded data
        extractor.process_downloaded_data()

def run_gui_mode():
    """Run in GUI mode"""
    root = tk.Tk()
    root.title("Lottery Information Downloader")
    
    controller = MainController()
    main_window = MainWindow(root, controller)
    main_window.pack(fill="both", expand=True, padx=10, pady=10)
    
    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description='Lottery Information Downloader')
    parser.add_argument('--gui', action='store_true', help='Run in GUI mode')
    parser.add_argument('--script', action='store_true', help='Run in script mode')
    args = parser.parse_args()

    # Default to GUI mode if no arguments provided
    if not (args.gui or args.script):
        args.gui = True

    if args.gui:
        run_gui_mode()
    else:
        run_script_mode()

if __name__ == "__main__":
    main()
