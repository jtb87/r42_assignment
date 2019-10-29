import logging
import boto3
from botocore.exceptions import ClientError


def upload_file(location, filename):
    s3 = boto3.client("s3")
    with open(location, "rb") as f:
        s3.upload_fileobj(f, "relay42assignment", filename)


loc = "./data_example.json"

upload_file(loc, "data_example.json")
