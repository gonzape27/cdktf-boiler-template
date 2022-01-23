#!/usr/bin/env python

from imports.aws import wafv2
from functions.utils import *

def create_wafv2 ():
    my_waf = wafv2.Wafv2WebAcl(
                global_variables.id_self,
                global_variables.my_id+"-wafv2",
                name = global_variables.default_name+"-WAFWebACL", 
                default_action = wafv2.Wafv2WebAclDefaultAction(
                   allow = {}
                ),
                scope = "CLOUDFRONT",
                visibility_config = wafv2.Wafv2WebAclVisibilityConfig(
                    cloudwatch_metrics_enabled = True,
                    metric_name = global_variables.default_name+"-MetricForWebACL",
                    sampled_requests_enabled = True
                ),
                rule = [
                    {
                        "name": "AWS-AWSManagedRulesCommonRuleSet",
                        "priority": 1,
                        "statement": {
                            "managedRuleGroupStatement": {
                                "vendorName": "AWS",
                                "name": "AWSManagedRulesCommonRuleSet"
                            }
                        },
                        "visibilityConfig": {
                            "sampledRequestsEnabled": True,
                            "cloudwatchMetricsEnabled": True,
                            "metricName": global_variables.default_name+"-AWSManagedRulesCommonRuleSet"
                        },
                        'overrideAction': {
                             'none': {}
                        }
                    },
                    {
                        "name": "AWS-AWSManagedRulesSQLiRuleSet",
                        "priority": 2,
                        "statement": {
                            "managedRuleGroupStatement": {
                                "vendorName": "AWS",
                                "name": "AWSManagedRulesSQLiRuleSet"
                            }
                        },
                        "visibilityConfig": {
                            "sampledRequestsEnabled": True,
                            "cloudwatchMetricsEnabled": True,
                            "metricName": global_variables.default_name+"-AWSManagedRulesSQLiRuleSet"
                        },
                        'overrideAction': {
                             'none': {}
                        }
                    },
                    {
                        "name": "AWS-AWSManagedRulesBotControlRuleSet",
                        "priority": 3,
                        "statement": {
                            "managedRuleGroupStatement": {
                                "vendorName": "AWS",
                                "name": "AWSManagedRulesBotControlRuleSet"
                            }
                        },
                        "visibilityConfig": {
                            "sampledRequestsEnabled": True,
                            "cloudwatchMetricsEnabled": True,
                            "metricName": global_variables.default_name+"-AWSManagedRulesBotControlRuleSet"
                        },
                        'overrideAction': {
                             'none': {}
                        }
                    }
                ],
                tags = global_variables.my_tags           
             )
    return my_waf