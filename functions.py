import logging
import os
from datetime import datetime
import boto3
import time
import requests
import json

# Time the script is run

def timestamp():
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
    

def extract(data_directory: str):
    """
    Extracts data from the TfL Bike point API.

    Arguments:

    data_directory = the name of the folder to which data will be saved
    
    """

    # Variables
    attempt = 0
    max_retry = 5
    delay = 10
    filename = f'{data_directory}/{timestamp}.json'
    url = 'https://api.tfl.gov.uk/BikePoint/'

    # Logger
    logger=logging.getLogger()

    # Get data from the API - will cycle through attempts unless a 3xx or 4xx error is received
    while attempt < max_retry:
        attempt+=1
        logger.info(f'Attempt {attempt}')
        response = requests.get(url)
        status_code = response.status_code
        if 200 <= status_code < 300:
            data = response.json()
            if len(data) > 0:
                try:
                    with open(filename,'w') as file:
                        json.dump(data,file)
                    print('Data extracted successfully!')
                    logger.info(f'File {filename} successfully saved')
                    break
                except Exception as e:
                    logger.error(f'An error occurred: {e}')
            else:
                print('No data returned!')
                logger.error('No data returned')
                break

        elif status_code <= 100 or status_code >= 500:
            print(f'Error - retrying in 10s attempt {attempt}')
            logger.warning(f'Error - retrying in 10s attempt {attempt}')
            time.sleep(delay)
        else:
            print(f'API Error Code {status_code} - cancelled')
            logger.error(f'Bad response from API. Error code {status_code}')
            break

def load(AWS_ACCESS_KEY: str, AWS_SECRET_KEY: str, AWS_BUCKET_NAME: str, data_directory: str):
    """
    Loads locally saved data to a specified s3 bucket

    Arguments:
    
    aws_access_key (str) = AWS access Key
    aws_secret_key (str) = AWS API Secret
    aws_bucket_name (str) = AWS s3 bucket name
    data_directory (str) = directory where files to be uploaded exist
    
    """

    # Logger
    logger=logging.getLogger()

     # Configure AWS client
    s3_client = boto3.client(
        's3',
        aws_access_key_id = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_KEY
    )

    # Loop through data
    for file in os.listdir(data_directory):
        to_upload = f'{data_directory}/{file}'
        try:
            s3_client.upload_file(to_upload,AWS_BUCKET_NAME,file)
            logger.info(f'{file} successfully uploaded')
            print(f'{file}')
            os.remove(to_upload)
            logger.info(f'{file} deleted')
        except Exception as e:
            logger.exception(e)
