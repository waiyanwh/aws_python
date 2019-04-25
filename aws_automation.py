import boto3
import botocore.exceptions as ClientError
ec2 = boto3.resource('ec2')

# create VPC
vpc = ec2.create_vpc(CidrBlock='172.16.0.0/16')

# assign a name to our VPC
vpc.create_tags(Tags=[{"Key": "Name", "Value": "container_vpc"}])
vpc.wait_until_available()

# enable public dns hostname so that we can SSH into it later
ec2Client = boto3.client('ec2')
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )
print("vpc id = {} is created Successfully.".format(vpc.id))

# create an internet gateway and attach it to VPC
internetgateway = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)
internetgateway.create_tags(Tags=[{"Key": "Name", "Value": "container_internetgateway"}])
print("vpc {} is attached to internet gateway {} successfully.".format(vpc.id,internetgateway.id))

# create a route table and a public route
routetable = vpc.create_route_table()
route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)
routetable.create_tags(Tags=[{"Key": "Name", "Value": "container_routetable"}])
print("Routing table {} is created successfully.".format(routetable.id))

# create subnet and associate it with route table
subnet = ec2.create_subnet(CidrBlock='172.16.1.0/24', VpcId=vpc.id)
print("subnet {} created successfully.".format(subnet.id))
subnet.create_tags(Tags=[{"Key": "Name", "Value": "container_subnet"}])
routetable.associate_with_subnet(SubnetId=subnet.id)

# Create a security group and allow SSH inbound rule through the VPC
securitygroup = ec2.create_security_group(GroupName='SSH-ONLY', Description='only allow SSH traffic', VpcId=vpc.id)
securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=80, ToPort=80)
securitygroup.create_tags(Tags=[{"Key": "Name", "Value": "container_securitygroup"}])
print("Security group {} is created successfully".format(securitygroup.id))

# create a file to store the key locally
outfile = open('/home/wywh/key/ec2-keypair.pem', 'w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)
print("{}.pem for SSH login is created  successfully.".format(key_pair.name))

# create instance with security group
instances = ec2.create_instances(
 ImageId='ami-0044ba2d261f0e97f',
 InstanceType='t2.micro',
 MaxCount=1,
 MinCount=1,
 NetworkInterfaces=[{
 'SubnetId': subnet.id,
 'DeviceIndex': 0,
 'AssociatePublicIpAddress': True,
 'Groups': [securitygroup.group_id]
 }],
 KeyName='ec2-keypair')
instances[0].create_tags(Tags=[{"Key": "Name", "Value": "container box"}])
instances[0].wait_until_running()
print("Instance {} is created successfully".format(instances[0].id))

# allocate elastic ip for instances
RUNNING_INSTANCE_ID=[]
for instance in ec2.instances.all():
    if instance.state["Name"] == "running":
        RUNNING_INSTANCE_ID.append(instance.id)
        try:
            for i in RUNNING_INSTANCE_ID:
                allocation = client.allocate_address(Domain='vpc')
                response = client.associate_address(AllocationId=allocation['AllocationId'],InstanceId=i)
                print(response)
        except ClientError as e:
            print(e)
