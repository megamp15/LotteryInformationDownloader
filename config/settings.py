import os
from datetime import datetime

# Base URLs
BASE_URL = "https://txs.lotteryservices.com/RetailerWizard/#"

# Credentials (should be moved to environment variables in production)
LOGIN_EMAIL = "mpkasar@gmail.com"
LOGIN_PASSWORD = "TX786110."

# File paths
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")

# Timeouts
DEFAULT_WAIT_TIME = 10
DEFAULT_SLEEP_TIME = 2

# Date ranges
DEFAULT_START_DATE = "11/01/2024"
DEFAULT_END_DATE = "11/30/2024"

# Report types
REPORT_TYPES = {
    "PACK_INVENTORY": "Pack Inventory",
    "PACKS_ACTIVATED": "Packs Activated",
    "FULL_STATEMENT": "Full Statement"
} 