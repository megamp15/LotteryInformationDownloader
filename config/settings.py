import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URLs
BASE_URL = os.getenv('BASE_URL')

# Credentials
LOGIN_EMAIL = os.getenv('LOGIN_EMAIL')
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD')
RETAILER_NUM = os.getenv('RETAILER_NUM')

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed_data")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archived_data")

# Timeouts
DEFAULT_WAIT_TIME = 10
DEFAULT_SLEEP_TIME = 2

# Date ranges
DEFAULT_START_DATE = os.getenv('DEFAULT_START_DATE')
DEFAULT_END_DATE = os.getenv('DEFAULT_END_DATE')

# Report types
REPORT_TYPES = {
    "PACK_INVENTORY": "Pack Inventory",
    "PACKS_ACTIVATED": "Packs Activated",
    "FULL_STATEMENT": "Full Statement"
} 