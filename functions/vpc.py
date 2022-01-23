#!/usr/bin/env python

from imports.aws import vpc, ec2
from functions.utils import *

class VPC:
    id=global_variables.id_self,
    vpcId=global_variables.my_id+"vpc",
    cidr_block = "10.101.0.0/16",
    enable_dns_hostnames = True,
    enable_dns_support = True,
    tags=global_variables.my_tags

class VPC_2(VPC):
    id2="pepe"
var_vpc=VPC()


def get_parameters():
  print(all parameter)
  
  
def create_new_vpc():
    my_vpc = vpc.Vpc(
                var_vpc.id,
                var_vpc.vpcId,
                var_vpc.cidr_block,
                var_vpc.enable_dns_hostnames,
                var_vpc.enable_dns_support,
                var_vpc.tags
             )

    my_subnet_pvt = vpc.Subnet(
                         global_variables.id_self,
                         global_variables.my_id+"subnet_pvt_a",
                         vpc_id = var_vpc.id,
                         cidr_block = "10.101.0.0/19",
                         availability_zone = "us-east-1a",
                         tags=var_vpc.tags
                      )

    my_subnet_pub = vpc.Subnet(
                         global_variables.id_self,
                         global_variables.my_id+"subnet_pub_a",
                         vpc_id = var_vpc.id,
                         cidr_block = "10.101.128.0/19",
                         availability_zone = "us-east-1a",
                         tags=var_vpc.tags
                      )

    my_internet_gw = vpc.InternetGateway(
                       global_variables.id_self,
                       global_variables.my_id+"internet_gw",
                       vpc_id = var_vpc.id,
                       tags=var_vpc.tags
                    )

    my_elastic_ip = ec2.Eip(
                        global_variables.id_self,
                        global_variables.my_id+"eip",
                        vpc = True,
                        tags=var_vpc.tags
                    )

    my_nat_gw = vpc.NatGateway(
                       global_variables.id_self,
                       global_variables.my_id+"nat_gw",
                       subnet_id = my_subnet_pub.id,
                       allocation_id = my_elastic_ip.id,
                       tags=var_vpc.tags
                   )

    my_route_pvt_a = vpc.Route(
                        global_variables.id_self,
                        global_variables.my_id+"routepvt_a",
                        route_table_id = "rt-us-east-2-"+global_variables.default_name+"-privateA",
                        destination_cidr_block = "0.0.0.0/0",
                        nat_gateway_id = my_nat_gw.id
                     )
    
    my_route_pvt_b = vpc.Route(
                        global_variables.id_self,
                        global_variables.my_id+"routepvt_b",
                        route_table_id = "rt-us-east-2-"+global_variables.default_name+"-privateB",
                        destination_cidr_block = "0.0.0.0/0",
                        nat_gateway_id = my_nat_gw.id
                     )
    
    my_route_pub = vpc.Route(
                        global_variables.id_self,
                        global_variables.my_id+"routepub",
                        route_table_id = "rt-us-east-2-"+global_variables.default_name+"-public",
                        destination_cidr_block = "0.0.0.0/0",
                        gateway_id = my_internet_gw.id
                     )

    my_private_network_acl = vpc.NetworkAcl(
                                global_variables.id_self,
                                global_variables.my_id+"networkacl_pvt",
                                vpc_id = var_vpc.id,
                                subnet_ids= [ my_subnet_pvt.id ],
                                ingress = [
                                    vpc.NetworkAclIngress(
                                        rule_no = 110,
                                        action = "ALLOW",
                                        cidr_block = "10.0.0.0/8",
                                        protocol = "-1",
                                        from_port = 0,
                                        to_port = 0
                                    ),
                                    vpc.NetworkAclIngress(
                                        rule_no = 120,
                                        action = "ALLOW",
                                        cidr_block = "0.0.0.0/0",
                                        protocol = "TCP",
                                        from_port = 1024,
                                        to_port = 65535
                                    )
                                ],
                                egress = [
                                    vpc.NetworkAclEgress(
                                        rule_no = 210,
                                        action = "ALLOW",
                                        protocol = "TCP",
                                        cidr_block = "0.0.0.0/0",
                                        from_port = 1,
                                        to_port = 65535
                                    )
                                ],
                                tags=var_vpc.tags
                              )
    
    my_public_network_acl = vpc.NetworkAcl(
                                global_variables.id_self,
                                global_variables.my_id+"networkacl_pub",
                                vpc_id = var_vpc.id,
                                subnet_ids = [ my_subnet_pub.id ],
                                ingress = [
                                    vpc.NetworkAclIngress(
                                        rule_no = 110,
                                        action = "ALLOW",
                                        cidr_block = "0.0.0.0/0",
                                        protocol = "TCP",
                                        from_port = 1,
                                        to_port = 65535
                                    )
                                ],
                                egress = [
                                    vpc.NetworkAclEgress(
                                        rule_no = 210,
                                        action = "ALLOW",
                                        protocol = "TCP",
                                        cidr_block = "0.0.0.0/0",
                                        from_port = 1,
                                        to_port = 65535
                                    )
                                ],
                                tags=var_vpc.tags
                              )

    vpc.RouteTableAssociation(
        global_variables.id_self,
        global_variables.my_id+"assoc_pvt_a",
        route_table_id = my_route_pvt_a.id,
        subnet_id = my_subnet_pvt.id
    )

    vpc.RouteTableAssociation(
        global_variables.id_self,
        global_variables.my_id+"assoc_pvt_b",
        route_table_id = my_route_pvt_b.id,
        subnet_id = my_subnet_pvt.id
    )

    vpc.RouteTableAssociation(
        global_variables.id_self,
        global_variables.my_id+"assoc_pub_a",
        route_table_id = my_route_pub.id,
        subnet_id = my_subnet_pub.id
    )