import pandas as pd
import logging
from utils.file_manager import FileManager

logger = logging.getLogger(__name__)

class BaseDataProcessor:
    def __init__(self):
        self.file_manager = FileManager()
        self.file_manager.ensure_directories()

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