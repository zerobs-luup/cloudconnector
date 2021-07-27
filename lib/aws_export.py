#!venv/bin/python3
#
#
#

import argparse
import os
from AWS import AWS
import yaml
all_credential = ""

with open(os.environ["HOME"] + '/.aws/credentials') as f:
    all_credential = f.read()




def start_scan(profile):
    print("************* Searching for '"+profile+"' profile ****************")
    aws = AWS(profile)
    aws.start_scan()
    aws.save_result()


parser = argparse.ArgumentParser(description='AWS exporter to export ips from given credentials in ~/.aws/credentials.')

parser.add_argument('--profile', help="Please provide profile name to continue.",required=False)
parser.add_argument('--configFile', help="Please provide config file name to continue",required=False)




args = parser.parse_args()
if args.profile is None and args.configFile is None:
    parser.error("Please provide one of the following aws profile name to continue : \n\n" + all_credential)

if args.configFile is not None:
    stream = open("config.yaml", 'r')
    config = yaml.load(stream, Loader=yaml.FullLoader)

    for profile in config["aws"]["client-names"]:
        start_scan(profile)

else:
    start_scan(args.profile)

