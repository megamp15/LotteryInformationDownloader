from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
import logging
import chromedriver_autoinstaller
import sys

logger = logging.getLogger(__name__)

class WebDriverSetup:
    @staticmethod
    def get_driver(mode='--script', company_name=None, download_path=None):
        """
        Configure and return Chrome WebDriver with appropriate download settings
        """
        # Install ChromeDriver and get its path
        chromedriver_path = chromedriver_autoinstaller.install()

        # Add ChromeDriver to PATH if on Windows and not already in PATH
        if sys.platform.startswith('win') and chromedriver_path not in os.environ['PATH']:
            os.environ['PATH'] += os.pathsep + os.path.dirname(chromedriver_path)

        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Configure download preferences based on mode
        if mode == '--script':
            # Create downloads/raw/COMPANY_NAME folder if it doesn't exist
            company_download_path = os.path.join('downloads', 'raw', company_name)
            os.makedirs(company_download_path, exist_ok=True)
            download_dir = os.path.abspath(company_download_path)
        else:  # GUI mode
            # Create raw/COMPANY_NAME folder in user-selected directory
            company_download_path = os.path.join(download_path, 'raw', company_name) if company_name else download_path
            os.makedirs(company_download_path, exist_ok=True)
            download_dir = os.path.abspath(company_download_path)
            
        # Set comprehensive download preferences
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
        driver.set_window_size(1024, 768)
        wait = WebDriverWait(driver, 120)
        
        return driver, wait
