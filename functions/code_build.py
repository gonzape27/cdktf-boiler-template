#!/usr/bin/env python

from imports.aws import codebuild
from cdktf import Fn
from functions.utils import *
from functions.ssm import create_new_string_parameter,create_array_string_parameter

def create_codebuild_project (  service_role, cloudfront_hosted_zone_id):
   
    # Env Vars Dict
    my_env_var_dic_path = "files/"+global_variables.repository_name+".conf"

    # Add SSM Parameters 
    ssm_vars=get_ssm_variables(my_env_var_dic_path)
    create_array_string_parameter(global_variables.id_self, global_variables.my_id,ssm_vars)

    # Add CodeBuild Project
    root_path="../../.."
    build_spec_path = Fn.abspath(root_path)+"/files/buildspec.yml.tftpl"
    build_spec_data = Fn.templatefile(path=build_spec_path, vars={ "PROJECT_NAME": global_variables.default_name, "DISTRIBUTION_ID": cloudfront_hosted_zone_id })

    code_vars=get_codepipeline_variables(my_env_var_dic_path)
    
    # Create an empty list
    env_var_list = []

    # Loop the Dictoriary and add to list.
    for key, value in code_vars.items():
      env_var_list.append( 
          codebuild.CodebuildProjectEnvironmentEnvironmentVariable(
                name=key,
                value=value,
                type="PARAMETER_STORE"
          )
      )

    codebuild_project = codebuild.CodebuildProject(
                            global_variables.id_self,
                            global_variables.my_id+"codebuild",
                            name = global_variables.default_name+"-cloudfront-s3-deploy",
                            service_role = service_role,
                            source = codebuild.CodebuildProjectSource(
                               type="CODEPIPELINE",
                               buildspec=build_spec_data
                            ),
                            environment = codebuild.CodebuildProjectEnvironment(
                                compute_type= "BUILD_GENERAL1_SMALL",
                                type = "LINUX_CONTAINER",
                                image = "aws/codebuild/amazonlinux2-x86_64-standard:3.0",
                                environment_variable = env_var_list
                            ),
                            logs_config = codebuild.CodebuildProjectLogsConfig(
                               cloudwatch_logs = codebuild.CodebuildProjectLogsConfigCloudwatchLogs(
                                    group_name  = "log-group",
                                    stream_name = "log-stream"
                               ),
                               s3_logs = codebuild.CodebuildProjectLogsConfigS3Logs(
                                   status="DISABLED"
                               )
                            ),
                            artifacts = codebuild.CodebuildProjectArtifacts(
                                type = "CODEPIPELINE"
                            ),
                            tags=global_variables.my_tags
    )
    return codebuild_project