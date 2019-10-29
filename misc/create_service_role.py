# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

# Requires boto3 1.9.72
import boto3, json

# Create IAM client
iam = boto3.client("iam")

path = "/"
role_name = "elastic-beanstalk-sqs-role"
description = "sqs-s3-eb full-access"


def create_policy():
    try:
        with open("./misc/service_role.json", "r") as trust_policy:
            tp = json.load(trust_policy)
            response = iam.create_role(
                Path=path,
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(tp),
                Description=description,
                MaxSessionDuration=3600,
            )
            print(response)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    create_policy()
