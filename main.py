import tkinter as tk
import argparse
import logging
from gui.views.main_window import MainWindow
from gui.controllers.main_controller import MainController
from core.data_extractor import DataExtractor, browser_session
from config.settings import *
from utils.webdriver_setup import WebDriverSetup

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_script_mode():
    """Run in script mode"""
    logger.info("Starting script mode")
    
    for retailer in RETAILERS_DATA:
        # Create WebDriver with script mode settings
        driver, wait = WebDriverSetup.get_driver(
            mode='--script',
            company_name=retailer["company_name"]
        )
        
        try:
            extractor = DataExtractor(
                driver, 
                wait, 
                mode='--script',
                company_name=retailer["company_name"],
                download_path='downloads'
            )
            extractor.add_retailer(
                retailer["retailer_number"], 
                retailer["company_name"]
            )
            
            # Navigate to login page
            logger.info(f"Navigating to login page for {retailer['company_name']}")
            extractor.login_page.navigate_to()
            
            # Attempt login
            logger.info(f"Attempting login for {retailer['company_name']}")
            login_success = extractor.login_page.login(LOGIN_EMAIL, LOGIN_PASSWORD)
            
            if not login_success:
                logger.error(f"Login failed for {retailer['company_name']} - skipping to next retailer")
                continue
            
            # Process retailer if login successful
            extractor.process_all_retailers()
            
        except Exception as e:
            logger.error(f"Error processing {retailer['company_name']}: {str(e)} - skipping to next retailer")
            continue
        finally:
            driver.quit()

def run_gui_mode():
    """Run in GUI mode"""
    root = tk.Tk()
    root.title("Lottery Information Downloader")
    
    controller = MainController(root)
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
