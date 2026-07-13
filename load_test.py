from dotenv import load_dotenv
import os
import boto3

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Check that dotenv is configured correctly
#print(AWS_BUCKET_NAME)

s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_KEY
)

data = 'data/2026-07-08_154505.json'
filename = '2026_07-08_154505.json'

s3_client.upload_file(data,AWS_BUCKET_NAME,filename)