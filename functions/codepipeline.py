#!/usr/bin/env python

from imports.aws import codepipeline
from functions.utils import *

def create_new_codepipeline(bucket_name, codePipelineRoleArn, codebuildName):
    code_pipeline = codepipeline.Codepipeline(
                        global_variables.id_self, 
                        global_variables.my_id+"cpline",
                        name = global_variables.default_name+"-s3-cloudfront-pipeline",
                        role_arn = codePipelineRoleArn,
                        artifact_store = [
                            codepipeline.CodepipelineArtifactStore(
                                location = bucket_name,
                                type = "S3"
                            )
                        ],
                        stage = [
                            codepipeline.CodepipelineStage(
                                name = "Source",
                                action = [
                                    codepipeline.CodepipelineStageAction(
                                        name = "Source",
                                        category = "Source",
                                        owner = "AWS",
                                        provider = "CodeStarSourceConnection",
                                        version = "1",
                                        output_artifacts = ['sourceOutput'],
                                        configuration = {
                                            "ConnectionArn": global_variables.my_codestar_arn,
                                            "FullRepositoryId": global_variables.full_repository_name,
                                            "BranchName": global_variables.branch
                                        }
                                    )
                                ]
                            ),
                            codepipeline.CodepipelineStage(
                                name = "Build",
                                action = [
                                    codepipeline.CodepipelineStageAction(
                                        name = "Build",
                                        category = "Build",
                                        owner = "AWS",
                                        provider = "CodeBuild",
                                        version = "1",
                                        input_artifacts = ['sourceOutput'],
                                        output_artifacts = ['buildOutput'],
                                        configuration = { "ProjectName": codebuildName }
                                    )
                                ]    
                            )
                        ],
                        tags=global_variables.my_tags
    )
    return code_pipeline