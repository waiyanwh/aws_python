#!/usr/bin/python
import boto3
KEY_NAME = 'testing1'
IMAGE_ID = "ami-0044ba2d261f0e97f"
TYPE = 't2.micro'
ec2 = boto3.resource('ec2')
)

# Create new EC2 Instance
instance = ec2.create_instances(
    ImageId=IMAGE_ID,
    MinCount=1,
    MaxCount=1,
    InstanceType=TYPE,
    KeyName=KEY_NAME
    NetworkInterfaces=[{'Group': []}]
)
