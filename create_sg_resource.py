import boto3
ec2 = boto3.resource('ec2')
ec2_client = boto3.client('ec2')
response_vpc = ec2_client.describe_vpcs()
vpc_id = response_vpc.get('Vpcs', [{}])[0].get('VpcId', '')
sec_group = ec2.create_security_group(
    GroupName='slice_0', Description='slice_0 sec group', VpcId=vpc_id)
sec_group.authorize_ingress(
    CidrIp='0.0.0.0/0',
    IpProtocol='tcp',
    FromPort=80,
    ToPort=80,
)
sec_group.authorize_ingress(
    CidrIp='0.0.0.0/0',
    IpProtocol='tcp',
    FromPort=22,
    ToPort=22,
)
print(sec_group.id)
