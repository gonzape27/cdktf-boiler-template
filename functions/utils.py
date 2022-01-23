#/usr/bin/env python

import os
import json

from dotenv import load_dotenv, find_dotenv

class get_variables:
    # Load Enviromental Variables from file
    load_dotenv(find_dotenv())
    branch="develop"
    my_id="sdk"
    domain_name="your-domain-name.tk"
    project=os.environ.get("PROJECT")
    env=os.environ.get("ENVIRONMENT")
    region=os.environ.get("REGION")
    profile=os.environ.get("PROFILE")    
    default_name= str(project) + "-" + str(env)
    repository_name = str("frontend")
    repository_root = "rootstrap"
    full_repository_name = repository_root+"/"+repository_name
    my_codestar_arn = "arn:aws:codestar-connections:sa-east-1:XXXXXX:connection/XXXXXX"
    my_tags={"Customer": default_name, "BillingId": default_name, "Company": "Your company Inc."}
    id_self="0"
    
global_variables=get_variables()
    
def get_ssm_variables(file):
    ssm_vars = {}
    with open(file) as f:
      for line in f.readlines():
        key, value = line.rstrip("\n").split("=")
        ssm_vars["/"+global_variables.default_name+"/"+global_variables.repository_name+"/"+key] = value
    return ssm_vars
    
def get_codepipeline_variables(file):
    code_vars = {}
    with open(file) as f:
      for line in f.readlines():
        key, value = line.rstrip("\n").split("=")
        code_vars["VAR_"+key] = "/"+global_variables.default_name+"/"+global_variables.repository_name+"/"+key
    return code_vars
    
    
