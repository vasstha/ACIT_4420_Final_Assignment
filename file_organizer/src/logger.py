import logging

logging.basicConfig(filename="file_organizer.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_error(error):
    """
    Logs errors to the log file.
    """
    logging.error(f"Error: {error}")
