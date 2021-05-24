import logging


def get_logger():
    """Returns the logger object with specified format."""
    FORMAT = "%(asctime)-15s [%(funcName)s] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger
