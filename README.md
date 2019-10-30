# R42 assignment
## Description of solution
See diagram 'relay42_diagram.png' 

Short description of the approach and limitations of the implementation.


Diagram:
![Screenshot](relay42_diagram.png)

## Source code deployable to dev/test/prod
The architecture is pretty much the same - it would mean setting different env variables.

## Deployment steps
So in all honesty this is the part where I got stuck a little bit. 
The creation of resources and deployment itself is pretty straightforward but making sure all the 
IAM roles are set-up correctly and triggers are done correctly was the issue.

I guess that it would make sense to look at something like cloudformation.
But here goes:

### 1 - Install AWS-CLI dependencies

pip install awsebcli
pip install boto3

IAM-role for programmatic access should contain the `AWSElasticBeanstalkFullAccess` and `AmazonSQSFullAccess` policies.

### 2 & 3 - Create s3/sqs resources 
Run the deployment scripts: 
- create_s3_bucket.py
- create_sqs_queue.py

### 4 - Deploy lambda file-handler & set up `s3ObjectCreated` event

Deploy code in `./lambda-file-handler` folder to lambda
Set up S3 event to trigger lambda function whenever file is created.

IAM-role for lambda function should contain the `AmazonSQSFullAccess` policy.

### 5 - Set up sqs-consumer on elastic-beanstalk
cd into /eb-sqs-consumer directory

Issue the following commands:
- eb init consumer-sqs -p python-3.6 -r eu-central-1
- eb create sqs-consumer-app --single -i t2.nano

IAM role for service should contain the `AmazonSQSFullAccess` policy

endpoints for es-service:
GET - eb-beanstalk.url.com/status   -- displays the status of the sqs-consumer
GET - eb-beanstalk.url.com/start    -- start the consumer
GET - eb-beanstalk.url.com/stop     -- stop the consumer
