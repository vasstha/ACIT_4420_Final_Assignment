import logging
from datetime import datetime

def setup_logger():
    logging.basicConfig(
        filename="route_optimizer.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger()
