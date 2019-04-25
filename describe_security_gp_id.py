import boto3
ec2 = boto3.client('ec2')

#response = ec2.describe_security_groups()
#sgp_id = response.get('SecurityGroups',[{}])[0].get('GroupId','')
def sg_id(id):
    ids = []
    sg_dict = ec2.describe_security_groups()
    s_groups = sg_dict['SecurityGroups']
    for i in s_groups:
        ids.append(i['GroupId'])
    for gp_id in ids:
        if gp_id == id:
            return gp_id
