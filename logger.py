import logging
import sys
from colorlog import ColoredFormatter
from datetime import date

today = str(date.today())
fileName = f"/mnt/n.haight/s3/emailAPI/logs/emailAPI-{today}.log"


def create_logger():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename=fileName,
        filemode='a',
        format='%(asctime)s -- %(levelname)s -- %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        )
    logger.setLevel(logging.DEBUG)

    # Define format for log entries
    formatter = ColoredFormatter(
        log_colors={
            'DEBUG': 'green',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        reset=True,
        secondary_log_colors={},
        style='%'
    )

    # Create console handler for log entries
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    return logger


logger = create_logger()
