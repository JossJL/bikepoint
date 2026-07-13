from dotenv import load_dotenv
import os
import boto3
import logging
from datetime import datetime

# env variables
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# variables

data_directory = 'data'
logging_directory = 'logs/load'
timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
logging_filename = f'{logging_directory}/{timestamp}.log'

# Create directory for logging
os.makedirs(logging_directory,exist_ok=True)

# Configure the logger
handlers=[
    logging.FileHandler(f"logs/amplitude_pipeline_{timestamp}.log"),  # Saves to file
    logging.StreamHandler()                        # Prints to terminal
]
logging.basicConfig(
    format = '%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=handlers
)

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
        logging.info(f'{file} successfully uploaded')
        print(f'{file}')
        os.remove(to_upload)
        logging.info(f'{file} deleted')
    except Exception as e:
        logging.exception(e)