import logging
import os
from .constants import Constants

# Ensure the log directory exists
log_dir = os.path.dirname(Constants.LOG_FILE_PATH)
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler

file_handler = logging.FileHandler(Constants.LOG_FILE_PATH)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# Get the root logger
logger = logging.getLogger()
logger.addHandler(file_handler)

# Example usage
if __name__ == "__main__":
    logger.info("Logger is configured and ready to use.")
