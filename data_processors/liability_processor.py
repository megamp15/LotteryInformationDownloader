import pandas as pd
from datetime import datetime, timedelta
import os
import logging
from .base_processor import BaseProcessor
from config.settings import DEFAULT_START_DATE, DEFAULT_END_DATE

logger = logging.getLogger(__name__)

class LiabilityProcessor(BaseProcessor):
    def __init__(self, download_dir, company_name):
        super().__init__(download_dir, company_name)
        
    def get_week_ranges(self, start_date_str, end_date_str):
        """Calculate week ranges from start to end date"""
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y')
        
        # Get first Saturday after start date
        days_to_saturday = (5 - start_date.weekday()) % 7
        first_saturday = start_date + timedelta(days=days_to_saturday)
        
        week_ranges = []
        current_start = start_date
        
        # Handle first partial week if needed
        if days_to_saturday > 0:
            week_ranges.append((
                current_start.strftime('%Y%m%d'),
                current_start.strftime('%Y-%m-%d'),
                first_saturday.strftime('%Y-%m-%d')
            ))
            current_start = first_saturday + timedelta(days=1)
        
        # Generate full week ranges
        while current_start <= end_date:
            week_end = min(current_start + timedelta(days=6), end_date)
            week_ranges.append((
                week_end.strftime('%Y%m%d'),
                current_start.strftime('%Y-%m-%d'),
                week_end.strftime('%Y-%m-%d')
            ))
            current_start = week_end + timedelta(days=1)
            
        return week_ranges
        
    def process_liability_data(self):
        """Process liability data from downloaded Excel file"""
        try:
            # Find the liability file in raw directory
            liability_files = [f for f in os.listdir(self.raw_dir) 
                             if 'Inventory_History' in f and f.endswith('.xlsx')]
            
            if not liability_files:
                logger.warning(f"No liability files found for {self.company_name}")
                return
            
            for file in liability_files:
                file_path = os.path.join(self.raw_dir, file)
                logger.info(f"Processing liability file: {file}")
                
                # Read Excel file
                df = pd.read_excel(file_path)
                
                # Sort by activated date
                df['Activated'] = pd.to_datetime(df['Activated'], errors='coerce')
                df = df.sort_values('Activated')
                
                # Remove rows without activated date
                df = df.dropna(subset=['Activated'])
                
                if df.empty:
                    logger.warning("No valid data found after filtering")
                    continue
                
                # Extract retailer number from filename
                retailer_number = None
                for part in file.split('_'):
                    if part.isdigit():
                        retailer_number = part
                        break

                # Get dynamic week ranges based on settings
                week_ranges = self.get_week_ranges(DEFAULT_START_DATE, DEFAULT_END_DATE)

                # Create separate CSV for each week range
                for week_end, start_date, end_date in week_ranges:
                    # Filter data for this week
                    mask = (df['Activated'] >= start_date) & (df['Activated'] <= end_date)
                    week_data = df[mask]
                    
                    if not week_data.empty:
                        output_file = f"inventoryHistory_{retailer_number}_{week_end}.csv"
                        output_path = os.path.join(self.processed_dir, output_file)
                        
                        # Save to CSV
                        week_data.to_csv(output_path, index=False)
                        logger.info(f"Created liability CSV for week ending {week_end}")
                
                # Don't remove the original file
                logger.info(f"Finished processing liability file: {file}")
                
        except Exception as e:
            logger.error(f"Error processing liability data: {str(e)}") 