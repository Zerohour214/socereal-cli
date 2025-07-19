"""Helpers for configuring application logging."""
import logging

def setup_logging():
    """Configure a basic console logger."""
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=logging.INFO
    )
