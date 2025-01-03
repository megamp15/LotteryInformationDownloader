import os
import pandas as pd
import logging
import shutil
from utils.file_manager import FileManager

logger = logging.getLogger(__name__)

class BaseProcessor:
    def __init__(self, download_dir, company_name, start_date=None, end_date=None):
        self.download_dir = download_dir
        self.company_name = company_name
        self.company_dir = os.path.join(download_dir, company_name)
        self.raw_dir = os.path.join(self.company_dir, 'raw')
        self.processed_dir = os.path.join(self.company_dir, 'processed')
        self.start_date = start_date
        self.end_date = end_date
        
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

    def rename_and_copy_files(self):
        """Rename files in the raw directory and copy them to the processed directory."""
        for filename in os.listdir(self.raw_dir):
            new_filename = filename

            # Rename statementSummaryLsp to STATEMENTSUMMARY
            if filename.startswith('statementSummaryLsp'):
                new_filename = 'STATEMENTSUMMARY' + filename[len('statementSummaryLsp'):]

            # Copy the renamed file to the processed directory
            if new_filename != filename:
                src_path = os.path.join(self.raw_dir, filename)
                dest_path = os.path.join(self.processed_dir, new_filename)
                shutil.copy(src_path, dest_path)
                logger.info(f"Copied and renamed file from {filename} to {new_filename}") 