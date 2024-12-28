import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URLs
BASE_URL = os.getenv('BASE_URL', 'https://txs.lotteryservices.com/RetailerWizard/#')

# Credentials
LOGIN_EMAIL = os.getenv('LOGIN_EMAIL')
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD')

# Parse retailer information from comma-separated strings
RETAILER_NUMBERS = [num.strip() for num in os.getenv('RETAILER_NUM', '').split(',')]
COMPANY_NAMES = [name.strip() for name in os.getenv('COMPANY_NAME', '').split(',')]

# Create retailers data list from the two lists
RETAILERS_DATA = [
    {"retailer_number": num, "company_name": name} 
    for num, name in zip(RETAILER_NUMBERS, COMPANY_NAMES)
]

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