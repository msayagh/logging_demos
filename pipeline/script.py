import logging
import random
import time

# Configure logging
logging.basicConfig(
    filename="/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Sample operations for varied log scenarios
def simulate_operation(i):
    operation_type = random.choice(['read', 'write', 'update', 'delete'])
    success = random.choice([True, True, True, False])  # Higher chance of success

    logging.info(f"Operation {operation_type.upper()}")

    if not success:
        logging.error(f"Operation {operation_type.upper()} failed")
        return

    # Simulate warnings
    if random.random() < 0.2:
        logging.warning(f"Operation {operation_type.upper()} completed with warnings")
    else:
        logging.info(f"Operation {operation_type.upper()} completed successfully")

    # Redundant logging (common in realistic scenarios)
    if random.random() < 0.3:
        logging.info(f"Duplicate log: Operation {operation_type.upper()} confirmed")


if __name__ == "__main__":
    for i in range(1, 1001):
        simulate_operation(i)
        time.sleep(random.uniform(0.1, 0.5))

    # Final error log after loop
    logging.error("Critical failure: database connection lost")
