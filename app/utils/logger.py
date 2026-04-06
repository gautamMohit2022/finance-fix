import logging
import sys

# Create a named logger for the whole app
logger = logging.getLogger("finance_app")
logger.setLevel(logging.INFO)

# Console handler — prints to terminal where uvicorn is running
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)
