import os
import logging


LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", default=logging.DEBUG)
LOGGING_PATH = "logs"
if not os.path.exists(LOGGING_PATH):
    os.mkdir(LOGGING_PATH)

LOGGING_FILE = "kgiop.log"


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_LEVEL)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    file_handler = logging.FileHandler(os.path.join(LOGGING_PATH, LOGGING_FILE))
    file_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
