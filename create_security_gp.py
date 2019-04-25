import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')
GP_NAME = 'Container_security_group'
applied_id = []
response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

try:
    response = ec2.create_security_group(GroupName='Container',
                                         Description='For Container',
                                         VpcId=vpc_id)
    security_group_id = response['GroupId']
    tag = ec2.create_tags(Resources=[security_group_id], Tags=[{'Key': 'Name', 'Value': GP_NAME }])
    print('Security Group Created {} in vpc {}'.format(security_group_id, vpc_id))

    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
        ])
    print('Ingress Successfully Set {}'.format(data))
    print('Group id is {}'.format(security_group_id))

except ClientError as e:
    print(e)
