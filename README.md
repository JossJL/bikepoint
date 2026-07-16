# **DES7 Bike Point Pipeline Project**

This is a pipeline we are building alongside coach Jenny to learn the fundamentals of data engineering. Use this ReadMe as a guide of our journey from Extraction to Output.

## **Extract**

Our data is sourced from the TfL BikePoint API, which can be accessed [here](https://api-portal.tfl.gov.uk/api-details#api=BikePoint&operation=BikePoint_GetAll). We developed a potential use case, where this data would be used to identify hotspots of bike usage overtime. This requires us to extract the API data at regular intervals & attach a timestamp.

This is performed by a function contained within the [extract.py](utils/extract.py) file, called by the [main.py](main.py) script.


## **Load**

After being saved locally, our data is loaded to Amazon S3 buckets.

This is performed by a function contained within the [load.py](utils/load.py) file, called by the [main.py](main.py) script.

## **Project Structure**

```
bikepoint_pipeline/
├── .env                    # Hidden environment variables (AWS credentials)
├── main.py                 # The main orchestration script
└── utils/                  # Core modules package
    ├── extract.py          # API interaction and local JSON saving
    ├── load.py             # Boto3 AWS S3 upload logic
    └── helpers.py          # Logging configuration and timestamp utilities
```

## **Prerequisites**

To run this pipeline, you will need the following installed and configured:

- Python 3.8+

- An active AWS Account with programmatic access (Access Key and Secret Key)

- An AWS S3 Bucket created and ready to receive data

## **Set-up & Installation**

Clone the git repository
```bash
git clone https://github.com/JossJL/bikepoint.git
cd bikepoint
```

Configure a virtual environment for package installation
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Install required dependencies
```bash
pip install requests boto3 python-dotenv
```

Configure environment variables
Create a .env in the root directory. Input your AWS credentials here

```bash
###

AWS_ACCESS_KEY = 'ACCESS_KEY_HERE'
AWS_SECRET_KEY = 'SECRET_HERE'
AWS_BUCKET_NAME = 's3-bucket-name'
AWS_REGION = 'aws-region'
```

## Usage

Once the environment has been configured, you can trigger the pipeling by running the main script:

```bash
python main.py
```