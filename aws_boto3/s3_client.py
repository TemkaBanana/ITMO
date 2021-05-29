#!/usr/bin/env python3

import boto3

s3 = boto3.client('s3')


buckets = s3.list_buckets()['Buckets']

for bucket in buckets:
    print(bucket['Name'])


BUCKET_NAME = "bucket-for-s3-client-0014"

s3.create_bucket(Bucket = BUCKET_NAME)

s3.upload_file(Bucket = BUCKET_NAME, Filename = "s3_client.py", Key = "test.py")

s3.download_file(BUCKET_NAME, "test.py", "s3_cl.py")

with open('s3_cl.py', 'wb') as f:
    s3.download_fileobj(BUCKET_NAME, 'test.py', f)


s3.delete_object(Bucket = BUCKET_NAME, Key = "test.py")


def get_all_versions(bucket, filename):
    s3 = boto3.client('s3')
    keys = ["Versions"]
    results = []
    for k in keys:
        response = s3.list_object_versions(Bucket=bucket)[k]
        to_delete = [r["VersionId"] for r in response if r["Key"] == filename]
    results.extend(to_delete)
    return results


for version in get_all_versions(BUCKET_NAME, 'test.py'):
    s3.delete_object(Bucket=BUCKET_NAME, Key='test.py', VersionId=version)



s3.delete_bucket(Bucket=bucket)
