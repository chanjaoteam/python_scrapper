import logging

def setup_logger():
    """Set up the logger for the scraper."""
    logging.basicConfig(
        filename='log/scraper.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log_info(message):
    """Log an informational message."""
    logging.info(message)

def log_error(message):
    """Log an error message."""
    logging.error(message)
