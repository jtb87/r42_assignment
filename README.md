
# step 1
pip install awsebcli
pip install boto3


# step 2
set up AWS credentials
# step 3



cd /eb-sqs-consumer
eb init consumer-sqs -p python-3.6 -r eu-central-1
eb create sqs-consumer-app --single -i t2.nano
eb use sqs-consumer-app
eb deploy sqs-consumer-app -l sqs-consumer-app-new
# set env variables
eb setenv REGION_NAME=eu-central-1 API_ENDPOINT=https://some.endpoint.com QUEUE_NAME=relay42.fifo

