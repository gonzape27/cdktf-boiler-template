#!/usr/bin/env python
from imports.aws import route53
from functions.utils import *

def create_hosted_zone():
    my_route53_zone = route53.Route53Zone(global_variables.id_self, global_variables.my_id+"-route53", name=global_variables.domain_name, tags=global_variables.my_tags)
    return my_route53_zone

def add_new_record (zone_id, name, type, ttl, records):
    my_route53_record = route53.Route53Record(
                                global_variables.id_self,
                                global_variables.my_id+"-r53record", 
                                zone_id=zone_id, 
                                name=name,
                                type=type,
                                ttl=ttl, records=records)
    return my_route53_record

def add_new_alias_record (zone_id,alias_domainName, alias_hostedZoneId):
    my_route53_alias_record = route53.Route53Record(
                                 global_variables.id_self, 
                                 global_variables.my_id+"-r53record-cf", 
                                 zone_id = zone_id, 
                                 name = global_variables.domain_name, 
                                 type = "A", 
                                 alias = [
                                     route53.Route53RecordAlias(
                                         name = alias_domainName,
                                         zone_id = alias_hostedZoneId,
                                         evaluate_target_health = True
                                     )
                                 ]
                              )
    return my_route53_alias_record    
    
    
