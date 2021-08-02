#!venv/bin/python3
#
#
#

import yaml
import sys
import json
import requests

from datetime import datetime

sys.path.append("lib")

from AWS import AWS
from AZURE import AZURE
from GPC import GPC
from DO import DO


# ~ from LUUP import IP_API


def usage():
  print("""

USAGE:

  %s -h     -> this help
  
  %s ping   -> test api_connection
  
  %s run    -> collect IPs and update LUUP_API
  
  
  """ % ("lcc", "lcc", "lcc"))

class RUN:
    config_file = None
    env = None

    results = {}
    total_ips = []

    def __init__(self, config_file):
        self.config_file = config_file
        a_yaml_file = open(self.config_file)
        self.env = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

    def api_test(self):
      self.luup_test()

    def start(self):
        self.aws()
        self.azure()
        self.gpc()
        self.do()
        self.save_result()
        self.send_to_luup()

    def aws(self):
        if self.env.get("aws") is not None:
            client_names = self.env.get("aws")["client-names"]

            print("\n**************************************************")
            print("\n****************   Scanning   AWS  ***************")
            print("\n**************************************************")
            self.results["aws"] = {}
            for client in client_names:
                aws = AWS(client)
                aws.start_scan()
                self.total_ips = self.total_ips + aws.public_ips + aws.private_ips

                self.results["aws"][client] = {"publicIps": aws.public_ips, "privateIps": aws.private_ips}

    def azure(self):
        if self.env.get("azure") is not None:
            print("\n**************************************************")
            print("\n**************** Scanning AZURE   **************")
            print("\n**************************************************")
            azure = AZURE(self.config_file)

            azure.start_scan()
            self.total_ips = self.total_ips + azure.public_ips
            self.results["azure"] = {"publicIps": azure.public_ips}


    def gpc(self):
        if self.env.get("gpc") is not None:
            print("\n**************************************************")
            print("\n******************** Scanning  GPC  ***************")
            print("\n**************************************************")

            project = self.env["gpc"]["token"]
            gcs = GPC(project)
            gcs.start_scan()
            self.total_ips = self.total_ips + gcs.public_ips + gcs.private_ips
            self.results["googleCloud"] = {"publicIps": gcs.public_ips, "privateIps": gcs.private_ips}

    def do(self):
        if self.env.get("digital-ocean") is not None:
            print("\n**************************************************")
            print("\n************* Scanning Digital Ocean  ************")
            print("\n**************************************************")

            do = DO(self.config_file)
            do.start_scan()
            self.total_ips = self.total_ips + do.public_ips
            self.results["digitalOcean"] = {"publicIps": do.public_ips}

    def save_result(self):

        now = datetime.now()

        timestamp = int(datetime.timestamp(now))
        file_name = "output/result." + str(timestamp) + ".json"
        f = open(file_name, "a")

        f.write(json.dumps(self.results, indent=4, sort_keys=True, default=str))
        f.close()
        print("*******************************************************************************************************")
        print("Data has been written to file : " + file_name + ". Please open the file to see result.")
        print("*******************************************************************************************************")

    def send_to_luup(self):
        if self.env.get("LUUP_API_KEY") is not None and self.env.get("LUUP_API_SERVER") is not None:
            headers = {"Authorization": "%s" % self.env.get("LUUP_API_KEY")}
            LUUP_URL = "%s" % self.env.get("LUUP_API_SERVER")
            ips  = list(filter(None.__ne__, self.total_ips))
            data  =  {
                "networks":ips,
                "as": []
            }
            res = requests.post("%s/api/v1/networks" % LUUP_URL, headers=headers, json=data)
            if res.status_code == 201:
              print("[+] Luup Updated: %s" % "OK | %s | %s" % (res.status_code, res.text) )
            elif res.status_code == 200:
              print("[+] Luup Unchanged: %s" % "OK | %s | %s" % ( res.status_code, res.text) )
            else:
              print("[-] Luup server response: %s" % "ERROR | %s | %s " % (res.status_code, res.text) )

    def luup_test(self):
        if self.env.get("LUUP_API_KEY") is not None and self.env.get("LUUP_API_SERVER") is not None:
            headers = {"Authorization": "%s" % self.env.get("LUUP_API_KEY")}
            LUUP_URL = "%s" % self.env.get("LUUP_API_SERVER")
            LUUP_API_ENDPOINT = "%s/api/v1/ping" % LUUP_URL 
            try:
              res = requests.get(LUUP_API_ENDPOINT, headers=headers)
            except Exception as e:
              print("\n[-] LUUP_API not available??? \n    API: %s \n    Error: \n\n%s" % (LUUP_URL, e))
              sys.exit()
              
            if res.status_code == 200:
              print("[+] Luup PING: %s" % "OK | %s | %s \n    API: %s" % ( res.status_code, res.text, LUUP_API_ENDPOINT) )
            else:
              print("[-] Luup server response: ERROR | %s | %s \n    API: %s" % (res.status_code, res.text, LUUP_API_ENDPOINT) )
      
        else:
            print("[-] ERROR Luup not configured yet, see config.yaml")


run = RUN("config.yaml")

try:
  action = sys.argv[1]
except:
  action = ""

if action == "run":
  run.start()
elif action == "ping":
  run.api_test()
else:
  usage()
  sys.exit()

# run.send_to_luup()
