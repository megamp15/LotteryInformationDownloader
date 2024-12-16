import os
import shutil
from datetime import datetime
import logging
from config.settings import DOWNLOAD_DIR, PROCESSED_DIR, ARCHIVE_DIR

logger = logging.getLogger(__name__)

class FileManager:
    @staticmethod
    def ensure_directories():
        """Ensure all required directories exist"""
        for directory in [DOWNLOAD_DIR, PROCESSED_DIR, ARCHIVE_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Created directory: {directory}")

    @staticmethod
    def get_latest_file(directory, pattern):
        """Get the most recently downloaded file matching the pattern"""
        files = [f for f in os.listdir(directory) if f.lower().endswith(pattern.lower())]
        if not files:
            return None
        return max([os.path.join(directory, f) for f in files], key=os.path.getctime)

    @staticmethod
    def move_file(src, dest_dir, new_name=None):
        """Move file to destination directory with optional renaming"""
        if new_name:
            dest = os.path.join(dest_dir, new_name)
        else:
            dest = os.path.join(dest_dir, os.path.basename(src))
        
        shutil.move(src, dest)
        logger.info(f"Moved file from {src} to {dest}")
        return dest

    @staticmethod
    def archive_file(file_path):
        """Move file to archive directory with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        new_name = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
        return FileManager.move_file(file_path, ARCHIVE_DIR, new_name) 