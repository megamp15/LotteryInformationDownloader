import os
import pandas as pd
import logging
from utils.file_manager import FileManager

logger = logging.getLogger(__name__)

class BaseProcessor:
    def __init__(self, download_dir, company_name):
        self.download_dir = download_dir
        self.company_name = company_name
        self.company_dir = os.path.join(download_dir, company_name)
        self.raw_dir = os.path.join(self.company_dir, 'raw')
        self.processed_dir = os.path.join(self.company_dir, 'processed')
        
        # Create directories if they don't exist
        for directory in [self.raw_dir, self.processed_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def read_csv(self, file_path):
        """Read CSV file with proper encoding and error handling"""
        try:
            return pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding='latin1')

    def read_excel(self, file_path):
        """Read Excel file"""
        return pd.read_excel(file_path)

    def save_dataframe(self, df, file_path):
        """Save DataFrame to file"""
        if file_path.endswith('.csv'):
            df.to_csv(file_path, index=False)
        elif file_path.endswith('.xlsx'):
            df.to_excel(file_path, index=False)
        logger.info(f"Saved processed data to {file_path}") 