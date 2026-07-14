import logging
import os
from datetime import datetime


# Time the script is run

def timestamp():
    """
    Creates a string of the local machine datetime

    """
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    return timestamp

# Function that configures the logger

def logger_setup(logging_directory: str):
    """
    Configures the logger to print to chosen directory.

    Arguments:

    logging_directory = the name of the folder to which logs will be saved
    
    """
    # Configure the logger
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    os.makedirs(logging_directory,exist_ok=True)

    handlers=[
        logging.FileHandler(f"{logging_directory}/bikepoint_pipeline_{timestamp}.log"),  # Saves to file
        logging.StreamHandler()                        # Prints to terminal
    ]
    logging.basicConfig(
        format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        level=logging.INFO,
        handlers=handlers
    )
    logging.info('Logger Initialised Successfully')
    return logging.getLogger()