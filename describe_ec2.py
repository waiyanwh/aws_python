#!/usr/bin/python3
import boto3
from botocore.exceptions import ClientError
RUNNING_INSTANCE_ID=[]
ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
    if instance.state["Name"] == "running":
        RUNNING_INSTANCE_ID.append(instance.id)
for i in RUNNING_INSTANCE_ID:
    print('{} is running'.format(i))
COUNT = len(RUNNING_INSTANCE_ID)
print(COUNT)
