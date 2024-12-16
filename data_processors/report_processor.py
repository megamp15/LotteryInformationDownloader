import pandas as pd
import os
from datetime import datetime
import logging
from .base_processor import BaseDataProcessor
from config.settings import DOWNLOAD_DIR, PROCESSED_DIR

logger = logging.getLogger(__name__)

class ReportProcessor(BaseDataProcessor):
    def __init__(self):
        super().__init__()
        self.report_types = {
            'pack_inventory': 'Pack Inventory',
            'packs_activated': 'Packs Activated'
        }

    def process_pack_inventory(self, file_path):
        """Process Pack Inventory report"""
        df = self.read_csv(file_path)
        
        # Add your processing logic here
        processed_df = df.copy()
        # Example: processed_df['Amount'] = processed_df['Amount'].astype(float)
        
        # Save processed file
        timestamp = datetime.now().strftime("%Y%m%d")
        processed_path = os.path.join(
            PROCESSED_DIR, 
            f"pack_inventory_processed_{timestamp}.csv"
        )
        self.save_dataframe(processed_df, processed_path)
        
        # Archive original file
        self.file_manager.archive_file(file_path)
        
        return processed_path

    def process_all_reports(self):
        """Process all downloaded reports"""
        for report_type in self.report_types:
            file_path = self.file_manager.get_latest_file(DOWNLOAD_DIR, '.csv')
            if file_path:
                logger.info(f"Processing {report_type} report")
                if report_type == 'pack_inventory':
                    self.process_pack_inventory(file_path)
                # Add other report types as needed 