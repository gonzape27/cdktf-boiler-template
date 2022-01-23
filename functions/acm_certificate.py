#!/usr/bin/env python

from imports.aws import acm
from functions.utils import *

def create_ssl_certificate ():
    ssl_certificate = acm.AcmCertificate(global_variables.id_self,
                                         global_variables.my_id+"-acmcert",
                                         domain_name=global_variables.domain_name,
                                         validation_method="DNS", tags=global_variables.my_tags)
    return ssl_certificate

def validate_ssl_certificate (certificate_arn, validation_record_fqdns):
    ssl_validation = acm.AcmCertificateValidation(global_variables.id_self,
                                                  global_variables.my_id+"-sslvalid",
                                                  certificate_arn=certificate_arn, 
                                                  validation_record_fqdns=validation_record_fqdns)
    return ssl_validation
    
    
