import logging
import time
from datetime import datetime
import requests
import json
import os

def extract(data_directory: str):
    """
    Extracts data from the TfL Bike point API.

    Arguments:

    data_directory = the name of the folder to which data will be saved
    
    """

    # Variables
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    attempt = 0
    max_retry = 5
    delay = 10
    filename = f'{data_directory}/{timestamp}.json'
    url = 'https://api.tfl.gov.uk/BikePoint/'

    # Logger
    logger=logging.getLogger()

    # Ensure the parent data directory exists
    os.makedirs(data_directory, exist_ok=True)

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