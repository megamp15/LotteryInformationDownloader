from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
import logging

logger = logging.getLogger(__name__)

class WebDriverSetup:
    @staticmethod
    def get_driver(mode='--script', company_name=None, download_path=None):
        """
        Configure and return Chrome WebDriver with appropriate download settings
        
        Args:
            mode (str): '--script' or '--gui' mode
            company_name (str): Company name for script mode downloads
            download_path (str): User-selected download path for GUI mode
        """
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # chrome_options.add_argument('--headless=new')
        
        # Configure download preferences based on mode
        if mode == '--script':
            # Create downloads/COMPANY_NAME folder if it doesn't exist
            company_download_path = os.path.join('downloads', company_name)
            os.makedirs(company_download_path, exist_ok=True)
            download_dir = os.path.abspath(company_download_path)
        else:  # GUI mode
            # Create COMPANY_NAME folder in user-selected directory
            company_download_path = os.path.join(download_path, company_name) if company_name else download_path
            os.makedirs(company_download_path, exist_ok=True)
            download_dir = os.path.abspath(company_download_path)
            
        # Set comprehensive download preferences (from old code)
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.automatic_downloads": 1
        }
            
        chrome_options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(3)
        wait = WebDriverWait(driver, 120)
        
        return driver, wait
