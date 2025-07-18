import logging

def setup_logging():
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=logging.INFO
    )
