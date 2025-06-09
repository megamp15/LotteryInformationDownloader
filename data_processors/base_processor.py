import os
import pandas as pd
import logging
import shutil
import re
from datetime import datetime
from utils.file_manager import FileManager

logger = logging.getLogger(__name__)

class BaseProcessor:
    def __init__(self, download_dir, company_name, start_date=None, end_date=None):
        self.download_dir = download_dir
        self.company_name = company_name
        self.raw_dir = os.path.join(download_dir, 'raw', company_name)
        self.processed_dir = os.path.join(download_dir, 'processed', company_name)
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

            # Rename pack_inventory files: 148616_Pack_Inventory_5-10-2025.csv -> PACK_INVENTORY_148616_20250510.csv
            elif 'Pack_Inventory' in filename:
                # Extract retailer number, date and extension
                match = re.match(r'(\d+)_Pack_Inventory_(\d+)-(\d+)-(\d+)\.(.+)', filename)
                if match:
                    retailer_num = match.group(1)
                    month = match.group(2).zfill(2)
                    day = match.group(3).zfill(2)
                    year = match.group(4)
                    extension = match.group(5)
                    new_filename = f'PACKINVENTORY_{retailer_num}_{year}{month}{day}.{extension}'

            # Rename packs_activated files: similar pattern to pack_inventory
            elif 'Packs_Activated' in filename or 'packs_activated' in filename.lower():
                # Handle both possible formats
                pattern = r'(\d+)_[Pp]acks_[Aa]ctivated_(\d+)-(\d+)-(\d+)\.(.+)'
                match = re.match(pattern, filename)
                if match:
                    retailer_num = match.group(1)
                    month = match.group(2).zfill(2)
                    day = match.group(3).zfill(2)
                    year = match.group(4)
                    extension = match.group(5)
                    new_filename = f'PACKSACTIVATED_{retailer_num}_{year}{month}{day}.{extension}'

            # Copy the renamed file to the processed directory
            if new_filename != filename:
                src_path = os.path.join(self.raw_dir, filename)
                dest_path = os.path.join(self.processed_dir, new_filename)
                shutil.copy(src_path, dest_path)
                logger.info(f"Copied and renamed file from {filename} to {new_filename}")
            else:
                # Copy file without renaming if no renaming rule applied
                src_path = os.path.join(self.raw_dir, filename)
                dest_path = os.path.join(self.processed_dir, filename)
                shutil.copy(src_path, dest_path)
                logger.info(f"Copied file {filename} to processed directory") 