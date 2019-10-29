# description
See diagram 'relay42_diagram.png' 

Short description of the approach and limitations of the implementation.


# Source code deployable to dev/test/prod
The architecture is pretty much the same - it would mean setting different env variables.

## Deployment steps
So in all honesty this is the part where I got stuck a little bit. 
The creation of resources and deployment itself is pretty straightforward but making sure all the 
IAM roles are set-up correctly and triggers are done correctly was the issue.

I guess that it would make sense to look at something like cloudformation.
But here goes: 
# step 1 - create virtual environment

pip install awsebcli
pip install boto3

(also make sure you have programmatic access to AWS with "AWSElasticBeanstalkFullAccess" and "AmazonSQSFullAccess")

# step 2 & 3 - Create s3/sqs resources 
pretty much run the deployment scripts: 
- create_s3_bucket.py && create_sqs_queue.py

# step 4 - deploy lambda function & set up trigger
nothing automated here :( 
deploy code '/lambda-file-handler

make sure the IAM role for this lambda has the policy "AmazonSQSFullAccess" attached

# setting up sqs-consumer
cd into /eb-sqs-consumer directory
issue the following commands:
- eb init consumer-sqs -p python-3.6 -r eu-central-1
- eb create sqs-consumer-app --single -i t2.nano

make sure the IAM role for this lambda has the policy "AmazonSQSFullAccess" attached

GET - eb-beanstalk.url.com/status -- will display the status
GET - eb-beanstalk.url.com/start -- will start the consumer
GET - eb-beanstalk.url.com/stop -- will stop the consumer
