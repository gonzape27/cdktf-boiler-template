#!/usr/bin/env python

from imports.aws import s3
from functions.utils import *

def create_new_bucket (bucket_name):
    my_bucket = s3.S3Bucket( global_variables.id_self, 
                                global_variables.my_id+"-s3bucket",
                                bucket=global_variables.default_name+"-"+bucket_name, 
                                acl="private", 
                                tags=global_variables.my_tags)
    return my_bucket

def create_s3_bucket_policy_json(bucketId, policyJson):
    my_bucket = s3.S3BucketPolicy(global_variables.id_self, global_variables.my_id+"sdk-bkpolicy", bucket=bucketId, policy=policyJson)
    return my_bucket
    
    
    
