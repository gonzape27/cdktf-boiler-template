#/usr/bin/env python

from imports.aws import ssm

def create_new_string_parameter(scope, id, name, value):
    ssm.SsmParameter(scope, id, name=name, type="String", value=value)
 
def create_array_string_parameter(scope, id, array):
    ssm_i = 0
    for key, value in array.items():
      create_new_string_parameter(scope, id+"ssm"+str(ssm_i), key, value)
      ssm_i = ssm_i + 1
