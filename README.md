# AWS_python
AWS (EC2) auto creation with python3 using boto3

Recommend using with python3

You can find [Here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html) for more info

## First of all
You need to install boto3 and aws-cli and botocore
Run the following comand to install this three packages
```
pip install boto3 --user
pip install aws-cli --user
pip install botocore
```
And configure aws-cli
```
aws configure
```
```
AWS Access Key ID [****************]: < YOUT_AWS_ACCESS_KEY_ID >
AWS Secret Access Key [****************]: < YOUT_AWS_SECRET_KEY >
Default region name []: < REGION_NAME or you can leave blank >
Default output format [None]: < leave blank >
```

## Notice
aws_automation.py is all in one package for creating 
* VPC creating
* Assigning name to vpc
* Enable public dns in vpc
* Creating internet gateway
* Creating routing table and public route
* Creating subnet
* Creating security group
* Generating key for instance login
* Creating instance with predefined security group 
* Allocating Elastic IP to instance

