import logging
import traceback
from datetime import datetime

# Configuration du logger
LOG_FILE = "app_errors.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,  # DEBUG pour tout logger
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(e: Exception, message: str = None):
    if message:
        logging.error(message)
    logging.error("Exception: %s", e)
    logging.error(traceback.format_exc())

def log_info(message: str):
    logging.info(message)

def log_warning(message: str):
    logging.warning(message)