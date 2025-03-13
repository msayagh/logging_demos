import os
import logging
import gzip
import shutil
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from datetime import datetime
from glob import glob

# Custom TimedRotatingFileHandler with gzip compression
class GzipTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        # Perform the usual rollover
        super().doRollover()
        
        log_files = glob(f"{self.baseFilename}.*")  # Find all files starting with baseFilename
        log_files = [f for f in log_files if not f.endswith(".gz")]  # Exclude already compressed files
        if log_files:
            latest_log_file = max(log_files, key=os.path.getctime)  # Get the most recent file by creation time
            
            # Compress the last rolled-over log file
            print("Compressing:", latest_log_file)
            with open(latest_log_file, 'rb') as f_in:
                with gzip.open(f"{latest_log_file}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(latest_log_file)  # Remove the uncompressed file

# Create 'logs' directory if it doesn't exist
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure the logger
logger = logging.getLogger("HelloWorldLogger")
logger.setLevel(logging.INFO)

# File handler for rotating logs every 30 seconds with gzip compression
time_handler = GzipTimedRotatingFileHandler("logs/app.log", when="s", interval=30)
time_handler.suffix = "%Y-%m-%d_%H-%M-%S"
time_handler.setLevel(logging.INFO)


# Log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
time_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(time_handler)

# Log some messages in a loop for demonstration
import time

for i in range(1000):
    logger.info(f"Hello, World! Log message {i + 1}")
    time.sleep(1)  # Sleep for 10 seconds to see the rolling effect
