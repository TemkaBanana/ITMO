#!/usr/bin/env python3


import boto3

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)



BUCKET_NAME = "bucket-for-s3-resource-0014"

s3.create_bucket(Bucket=BUCKET_NAME)

data = open('s3_resource.py', 'rb')
s3.Bucket(BUCKET_NAME).put_object(Key='test.py', Body=data)

for obj in s3.Bucket(BUCKET_NAME).objects.all():
    print(obj.key)



s3.Bucket(BUCKET_NAME).download_file(Key='test.py',Filename='s3_res.py')

s3.Object(bucket_name=BUCKET_NAME, key='test.py').delete()

for obj in s3.Bucket(BUCKET_NAME).objects.all():
    obj.delete()


s3.Bucket(name=BUCKET_NAME).object_versions.delete()

s3.Bucket(name=BUCKET_NAME).delete()
