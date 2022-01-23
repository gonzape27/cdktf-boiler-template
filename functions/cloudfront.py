#!/usr/bin/env python

from imports.aws import cloudfront
from functions.iam import create_new_s3_iam_document_policy
from functions.s3_simple_storage import create_s3_bucket_policy_json
from functions.utils import *


def create_cloudfornt_oai(s3bucketRegionalDomainName):
    cloudfront_oai = cloudfront.CloudfrontOriginAccessIdentity(global_variables.id_self, 
                                                               global_variables.my_id+"-oai",
                                                               comment=s3bucketRegionalDomainName)
    return cloudfront_oai

def create_cloudfront_distribution(s3BucketId, s3bucketName, s3BuckerArn, s3bucketRegionalDomainName, acmArn, wafv2Arn):
    
    # Generate OAI first
    cfIdentity = create_cloudfornt_oai(s3bucketRegionalDomainName)

    cloudfront_distribution = cloudfront.CloudfrontDistribution(
        global_variables.id_self,
        global_variables.my_id+"cf",
        aliases = [global_variables.domain_name],
        custom_error_response = [
            cloudfront.CloudfrontDistributionCustomErrorResponse(
                error_caching_min_ttl = 0,
                error_code = 404,
                response_code = 200,
                response_page_path = "/index.html"
            ),
            cloudfront.CloudfrontDistributionCustomErrorResponse(
                error_caching_min_ttl = 0,
                error_code = 403,
                response_code = 200,
                response_page_path = "/index.html"
            )
        ],
        default_cache_behavior = cloudfront.CloudfrontDistributionDefaultCacheBehavior(
            allowed_methods = ["GET", "HEAD"],
            cached_methods = ["GET", "HEAD"],
            compress = True,
            default_ttl = 43200,
            max_ttl = 86400,
            min_ttl = 0,
            smooth_streaming = False,
            target_origin_id = "S3-"+s3bucketName,
            viewer_protocol_policy = "redirect-to-https",
            forwarded_values = cloudfront.CloudfrontDistributionDefaultCacheBehaviorForwardedValues(
                cookies = cloudfront.CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies(
                    forward = "all"
                ),
                query_string = True
            )
        ),
        enabled = True,
        http_version = "http2",
        origin = [
            cloudfront.CloudfrontDistributionOrigin(
                domain_name = s3bucketRegionalDomainName,
                origin_id = "S3-"+s3bucketName,
                s3_origin_config = cloudfront.CloudfrontDistributionOriginS3OriginConfig(
                    origin_access_identity=cfIdentity.cloudfront_access_identity_path
                )
            )
        ],
        viewer_certificate = cloudfront.CloudfrontDistributionViewerCertificate(
            acm_certificate_arn = acmArn,
            ssl_support_method = "sni-only"
        ),
        restrictions = cloudfront.CloudfrontDistributionRestrictions(
            geo_restriction = cloudfront.CloudfrontDistributionRestrictionsGeoRestriction(
               restriction_type = "none"
            )
        ),
        web_acl_id = wafv2Arn,
        tags = global_variables.my_tags                   
    )

    my_iam_document = create_new_s3_iam_document_policy(s3BuckerArn, cfIdentity.iam_arn)
    my_bucket_policy = create_s3_bucket_policy_json(s3BucketId, my_iam_document.json)

    return cloudfront_distribution