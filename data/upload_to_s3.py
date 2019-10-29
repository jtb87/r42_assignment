import logging
import boto3
from botocore.exceptions import ClientError


def upload_file2(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(
            Filename=file_name, Key=file_name, Bucket=bucket
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(location, filename):
    s3 = boto3.client("s3")
    with open(location, "rb") as f:
        s3.upload_fileobj(f, "relay42assignment", filename)


loc = "./data_example.json"

upload_file(loc, "data_example.json")
