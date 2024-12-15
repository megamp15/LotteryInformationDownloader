from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import os

class WebDriverSetup:
    @staticmethod
    def get_driver():
        chrome_options = Options()
        
        # Set download preferences
        download_dir = os.path.join(os.getcwd(), "downloads")  # Creates a downloads folder in your project
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.automatic_downloads": 1
        }
        
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Create driver with options
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        return driver, wait
