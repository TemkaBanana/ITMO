#!/usr/bin/env python3

import boto3

rds = boto3.client('rds')

rds.create_db_instance(
    DBInstanceIdentifier="MYRDSPG",
    AllocatedStorage=200,
    DBName='MyRDSPostgresqlDB',
    Engine='postgres',
    StorageType='gp2',
    StorageEncrypted=True,
    AutoMinorVersionUpgrade=True,
    MultiAZ=False,
    MasterUsername='postgres',
    MasterUserPassword='secret',
    VpcSecurityGroupIds=['YOUR_SECURITY_GROUP_ID'],
    DBInstanceClass='db.m3.2xlarge',
    Tags=[{'Key': 'env', 'Value': 'prod'}],
)
