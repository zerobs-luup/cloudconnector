import boto3
import pyjq
import json
from datetime import datetime
import sys
import argparse
import os



class AWS:
    ec2 = ""
    private_ips = []
    public_ips = []
    err = ""
    aws_profile = ""

    def __init__(self, aws_profile):
        self.aws_profile = aws_profile
        try:
            ec2_session = boto3.Session(profile_name=aws_profile)
            self.ec2 = ec2_session.client('ec2')
        except:
            self.err = "Error: Profile '" + aws_profile + "' not found in ~/.aws/credentials"

    def start_scan(self):
        if self.err == "":
            regions = self.get_regions()
            instances = self.get_ec2_instances(regions=regions)
            self.public_ips = self.get_public_ip_addr(instances)
            self.private_ips = self.get_private_ip_addr(instances)
        else:
            print(self.err)

    def get_regions(self):
        raw_region = self.ec2.describe_regions()

        regions = pyjq.all('.Regions[]|.RegionName', raw_region)

        return regions

    def get_ec2_instances(self, regions):
        instances = []
        for region in regions:
            session = boto3.Session(profile_name="default", region_name=region)
            resource = session.resource(service_name="ec2")
            print("List of ec2 instances in from region", region)
            for each_in in resource.instances.all():
                print(each_in.id, each_in.state["Name"])
                instances.append(each_in.id)

        raw_describe_instances = self.ec2.describe_instances(
            InstanceIds=instances,
        )

        raw_describe_instances = json.loads(json.dumps(raw_describe_instances, indent=4, sort_keys=True, default=str))

        return raw_describe_instances

    def get_private_ip_addr(self, raw_describe_instances):
        return pyjq.all('.Reservations[]|.Instances[]|.NetworkInterfaces[]|.PrivateIpAddress', raw_describe_instances)

    def get_public_ip_addr(self, raw_describe_instances):
        return pyjq.all('.Reservations[]|.Instances[]|.PublicIpAddress', raw_describe_instances)

    def save_result(self):
        if self.err == "":
            now = datetime.now()

            timestamp = datetime.timestamp(now)
            file_name = "output/aws_" + str(timestamp) + "_" + self.aws_profile + ".json"
            f = open(file_name, "a")
            data = {"public_ips": self.public_ips, "private_ips": self.private_ips}

            f.write(json.dumps(data, indent=4, sort_keys=True, default=str))
            f.close()
            print("*************************************************************************************")
            print("Data has been written to file : "+file_name + ". Please open the file to see result.")
            print("*************************************************************************************")