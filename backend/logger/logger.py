# backend/data/logger/logger.py
import logging
import sys
from typing import Final

# Define Log Level (Read this from config.py later)
LOG_LEVEL: Final[str] = 'INFO' 

# Define the log format for better readability and structure
LOG_FORMAT: Final[str] = (
    "%(asctime)s | %(levelname)s | %(name)s | %(module)s:%(funcName)s:%(lineno)d - %(message)s"
)

def setup_logger(name: str = 'ai_copilot') -> logging.Logger:
    """
    Sets up and configures a centralized logger instance for the application.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Prevent logs from propagating to the root logger handlers (avoids duplicate output)
    logger.propagate = False 

    # Check if handlers are already set up to prevent duplicate logs (common issue in FastAPI)
    if not logger.handlers:
        # StreamHandler for console output (stdout)
        stream_handler = logging.StreamHandler(sys.stdout)
        
        formatter = logging.Formatter(LOG_FORMAT)
        stream_handler.setFormatter(formatter)
        
        logger.addHandler(stream_handler)
        
    return logger

# Create the main application logger instance
logger = setup_logger()