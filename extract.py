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

response = requests.get(url)
data = response.json()

os.makedirs('data',exist_ok=True)

with open(filename,'w') as file:
    json.dump(data,file)
print('done!')