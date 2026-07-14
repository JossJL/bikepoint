import logging
import os
import boto3


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
