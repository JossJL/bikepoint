#Libraries
import requests
from datetime import datetime
import os
import json
import logging
import time

#Variables
url = 'https://api.tfl.gov.uk/BikePoint/'
data_directory = 'data'
timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
filename = f'{data_directory}/{timestamp}.json'
max_retry = 5
attempt = 0
delay = 10

#Create data directory
os.makedirs(data_directory,exist_ok=True)

while attempt < max_retry:
    response = requests.get(url)
    status_code = response.status_code
    if 200 <= status_code < 300:
        data = response.json()
        with open(filename,'w') as file:
            json.dump(data,file)
        print('Data extracted successfully!')
        break
    elif status_code <= 100 or status_code >= 500:
        attempt+=1
        print(f'Error - retrying in 10s attempt {attempt}')
        time.sleep(delay)
    else:
        print(f'API Error Code {status_code} - cancelled')
        break
        
