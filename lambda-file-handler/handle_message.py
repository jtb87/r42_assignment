import json
import urllib.parse
import boto3
from uuid import uuid4
import hashlib
import os

queue_name = os.environ("QUEUE_NAME")

s3 = boto3.client("s3")
sqs = boto3.client("sqs", region_name="eu-central-1")
queue = sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]


def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        print("Error getting object {} from bucket {}.".format(key, bucket))
        raise e
    contents = response["Body"].read()
    message = json.loads(contents)
    handle_message(message=message)


def handle_message(message: dict):
    msg = anonamyze_message(message)
    publish_message_to_sqs(message=msg)


def publish_message_to_sqs(message):
    """ Send message to SQS queue """
    response = sqs.send_message(
        QueueUrl=queue,
        MessageAttributes={},
        MessageBody=json.dumps(message),
        MessageGroupId=str(uuid4()),
    )
    print(f"published message to sqs-queue: {response['MessageId']}")


def anonamyze_message(message):
    """ Replace identifiable data by hashed values."""
    for m in message["emails"]:
        m["email"] = anonamyze_value(m["email"])
        m["name"] = anonamyze_value(m["name"])
    return message


def anonamyze_value(value: str):
    data = value.encode("utf-8")
    sha512 = hashlib.sha256(data)
    sha512_hex_digest = sha512.hexdigest()
    return sha512_hex_digest

