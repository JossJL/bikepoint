# Libraries
import requests
from datetime import datetime
import os
import json
import logging
import time

# Variables
url = 'https://api.tfl.gov.uk/BikePoint/'
data_directory = 'data'
logging_directory = 'logs'
timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
filename = f'{data_directory}/{timestamp}.json'
logging_filename = f'{logging_directory}/{timestamp}.log'
max_retry = 5
attempt = 0
delay = 10

# Create directories
os.makedirs(data_directory,exist_ok=True)
os.makedirs(logging_directory,exist_ok=True)

# Setting up the logger
logging.basicConfig(
    filename = logging_filename,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger=logging.getLogger()
logger.info('Logging Initialised')

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
        
