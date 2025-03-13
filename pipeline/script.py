import logging
import time

# Configure logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Generate logs
if __name__ == "__main__":
    for i in range(10):
        logging.info(f"R2- Hello World Log {i}")
        time.sleep(1)

    logging.error("R2- This is an error message")
