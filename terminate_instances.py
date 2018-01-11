
import boto3

import boto3
ec2 = boto3.resource('ec2')

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
instanceListNames = []
attachedVolumes = []
for instance in instances:
    print(instance.id, instance.instance_type, instance.key_name, instance.private_ip_address, instance.public_dns_name ,instance.root_device_name)
    instanceListNames.append(instance.id)
    volumeId = instance.block_device_mappings
    attachedVolumes.append(volumeId[0]['Ebs']['VolumeId'])
    print(volumeId)

# Check budget
# Create a budget on AWS
# https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/budgets-create.html
# 
# Check your accoutn id
# https://docs.aws.amazon.com/IAM/latest/UserGuide/console_account-alias.html
# 

client = boto3.client('budgets')
response = client.describe_budget(
    AccountId='310130539075',
    BudgetName='BudgetInvestigation'
)

actualSpend = float(response['Budget']['CalculatedSpend']['ActualSpend']['Amount'])

print(actualSpend)


# If limit is exceeded create a snapshot of EBS and skill all instances

if(actualSpend > 0):
    print('create snapshot')
    print(attachedVolumes)
    '''
    for volumeId in attachedVolumes:
        ec2.create_snapshot(VolumeId=volumeId)
    '''
    print('kill all instances')
    print(instanceListNames)
    '''
    ec2.instances.filter(InstanceIds=instanceListNames).stop()
    ec2.instances.filter(InstanceIds=instanceListNames).terminate()
    '''
