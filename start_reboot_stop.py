import boto3
ec2 = boto3.resource('ec2')
ec2.Instance('< Put Instance ID here >').start()
ec2.Instance('< Put Instance ID here >').reboot()
ec2.Instance('< Put Instance ID here >').stop()