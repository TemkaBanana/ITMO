#!/usr/bin/env python3

import boto3
from time import sleep

client = boto3.client("ec2")

user_data = """#!bin/bash
sudo yum -y install httpd
sudo systemctl start httpd
"""

# launch instance
instance = client.run_instances(
    ImageId = '',
    MaxCount = 1,
    MinCount = 1,
    KeyName = 'DevOps',
    InstanceType = 't2.micro',
    SubnetId = '',
    UserData = user_data,
)

instance_id = instance['Instances'][0]['InstanceId']
sleep(10)
instance_ip_address = instance['Instances'][0]['PrivateIpAddress']
instance_state = client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['State']

print(f'\
      Launching instance:\
      Instance ID: {instance_id}\
      Instance IP address: {instance_state}\
     ')

while True:
    sleep(10)
    output = client.get_console_output(InstanceId=instance_id)
    boot_log = output.get('Output',None)
    if boot_log:
        break

print(output['Output'])

instance_state = client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['State']
print(f'Instance state: {instance_state}')

sleep(300)

client.terminate_instances(InstanceIds=[instance_id])

sleep(30)

output=client.get_console_output(InstanceId=instance_id)
print(output['Output'])

