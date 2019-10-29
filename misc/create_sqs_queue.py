import boto3

# Get the service resource
sqs = boto3.resource("sqs", region_name="eu-central-1")
# Create the queue. This returns an SQS.Queue instance
queue = sqs.create_queue(
    QueueName="relay43.fifo", Attributes={"DelaySeconds": "0", "FifoQueue": "true"}
)

print(queue.url)
