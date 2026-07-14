from dotenv import load_dotenv
import os
from utils.helpers import logger_setup
from utils.api_client import extract
from utils.aws_client import load

if __name__ == "__main__":

    # env variables
    load_dotenv()

    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

    # variables
    data_directory = 'data'

    logger_setup(logging_directory = 'logs')

    extract(data_directory = data_directory)

    load(
        AWS_ACCESS_KEY = AWS_ACCESS_KEY,
        AWS_SECRET_KEY = AWS_SECRET_KEY,
        AWS_BUCKET_NAME = AWS_BUCKET_NAME,
        data_directory = data_directory
    )



