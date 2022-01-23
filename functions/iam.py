#!/usr/bin/env python

from imports.aws import iam
from functions.utils import *

def create_new_iam_role (policyArnList, assumeRolePolicy):
    iam_role = iam.IamRole(
                        global_variables.id_self, 
                        global_variables.my_id+"cprole", 
                        name="codepipeline-role-2", 
                        managed_policy_arns=policyArnList,
                        assume_role_policy=assumeRolePolicy,
                        tags=global_variables.my_tags)
    return iam_role

def create_new_s3_iam_document_policy(bucketArn, CFoaiArn):

    iam_document_policy = iam.DataAwsIamPolicyDocument(
                        global_variables.id_self,
                        "sdk-docpolicy",
                        statement = [
                            iam.DataAwsIamPolicyDocumentStatement(
                                actions = [ "s3:GetObject" ],
                                resources = [ bucketArn+"/*" ],
                                principals = [
                                    iam.DataAwsIamPolicyDocumentStatementPrincipals(
                                        type = "AWS",
                                        identifiers = [ CFoaiArn ]
                                    )
                                ]
                            )
                        ]
    )
    return iam_document_policy
