import pandas as pd
import os
from datetime import datetime
import logging
from .base_processor import BaseProcessor
from config.settings import DOWNLOAD_DIR, PROCESSED_DIR

logger = logging.getLogger(__name__)

class ReportProcessor(BaseProcessor):
    def __init__(self, download_dir, company_name, start_date=None, end_date=None):
        super().__init__(download_dir, company_name, start_date, end_date)

    def process_report_data(self):
        """Process downloaded report data"""
        try:
            # Process files in raw directory but don't move them
            for filename in os.listdir(self.raw_dir):
                if filename.endswith('.csv'):
                    logger.info(f"Found report file: {filename}")
                    # Add any report processing logic here if needed
                    
        except Exception as e:
            logger.error(f"Error processing report data: {str(e)}") 