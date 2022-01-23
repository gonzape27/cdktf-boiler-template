#!/usr/bin/env python
import os
import json
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from imports.aws import AwsProvider
from cdktf import Fn
from functions.route_53 import create_hosted_zone,add_new_record,add_new_alias_record
from functions.s3_simple_storage import create_new_bucket
from functions.acm_certificate import create_ssl_certificate,validate_ssl_certificate
from functions.waf import create_wafv2
from functions.cloudfront import create_cloudfront_distribution
from functions.iam import create_new_iam_role
from functions.utils import *
from functions.code_build import create_codebuild_project
from functions.codepipeline import create_new_codepipeline
from functions.vpc import create_new_vpc

class MyStack(TerraformStack):
  def __init__(self, scope: Construct, ns: str):
    super().__init__(scope, ns)
    
    #Set Self id for Terraformstack to share among other functions
    global_variables.id_self=self
    
    # Configure AWS Provider, using specific profile
    AwsProvider(global_variables.id_self, 'aws', region=global_variables.region, profile=global_variables.profile)

    # Create Route53 Hosted Zone
    my_route53_zone = create_hosted_zone()

    # Create S3 Bucket
    my_s3_bucket = create_new_bucket("s3-cloudfront") 

    # Request new ACM certificate
    my_acm_certificate = create_ssl_certificate()
    
    # Add new Route 53 record
    my_route53_record = add_new_record(
                          my_route53_zone.zone_id,
                          Fn.one(my_acm_certificate.domain_validation_options("*").resource_record_name),
                          Fn.one(my_acm_certificate.domain_validation_options("*").resource_record_type),
                          14400,
                          [Fn.one(my_acm_certificate.domain_validation_options("*").resource_record_value)]
                        )

    # Validate the SSL certificate
    my_ssl_validation = validate_ssl_certificate(my_acm_certificate.arn, [my_route53_record.fqdn])

    # Create Wafv2 WebACL for CloudFront
    my_wafv2 = create_wafv2()

    # Create CloudFront Distribution
    my_cloudfront_distribution = create_cloudfront_distribution(
                                   my_s3_bucket.id,
                                   my_s3_bucket.bucket,
                                   my_s3_bucket.arn,
                                   my_s3_bucket.bucket_regional_domain_name, 
                                   my_acm_certificate.arn, 
                                   my_wafv2.arn
                                 )

    # Add Route53 record for CloudFront
    my_route53_cf_record = add_new_alias_record(
                             my_route53_zone.zone_id,
                             my_cloudfront_distribution.domain_name,
                             my_cloudfront_distribution.hosted_zone_id
                             )

    # Create new IAM Role: codepipeline-role
    my_policy_arn_list = [
                            'arn:aws:iam::aws:policy/AmazonS3FullAccess', 
                            'arn:aws:iam::aws:policy/CloudFrontFullAccess',
                            'arn:aws:iam::aws:policy/CloudWatchLogsFullAccess',
                            'arn:aws:iam::aws:policy/AmazonSSMFullAccess',
                            'arn:aws:iam::aws:policy/AWSCodePipelineFullAccess',
                            'arn:aws:iam::aws:policy/AWSCodeBuildAdminAccess'
                         ]

    my_assume_role_policy = Fn.jsonencode({
                                "Version": "2012-10-17",
                                "Statement": [
                                  {
                                    "Effect": "Allow",
                                    "Principal": {
                                      "Service": [
                                        "codebuild.amazonaws.com",
                                        "codepipeline.amazonaws.com"
                                      ]
                                    },
                                    "Action": "sts:AssumeRole"
                                  }
                                ]
                              })

    my_codepipeline_role = create_new_iam_role(my_policy_arn_list, my_assume_role_policy)

    
    my_codebuild_project = create_codebuild_project(
                             my_codepipeline_role.arn,
                             my_cloudfront_distribution.hosted_zone_id
                           )

    # CodePipeline
    my_codepipeline = create_new_codepipeline(
                        my_s3_bucket.bucket,
                        my_codepipeline_role.arn,
                        my_codebuild_project.name,
                        )


app = App()
MyStack(app, "cdktf-boiler-template")

app.synth()