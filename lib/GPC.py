import googleapiclient.discovery
import json
import pyjq
from datetime import datetime


class GPC:
    project = None
    zones = []
    compute = None
    public_ips = []
    private_ips = []

    def __init__(self, project):
        self.project = project
        self.compute = googleapiclient.discovery.build('compute', 'v1')
        self.get_zones()

    def start_scan(self):
        for zone in self.zones:
            print("Seaching in zone:"+zone)
            result = self.list_instances(self.compute,self.project,zone)
            if result is not None:
                print("+++++++++ Found results +++++++++++")
                self.public_ips.append(self.get_public_ip_addr(result))
                self.private_ips =  self.get_private_ip_addr(result)

    def get_zones(self):
        result = self.compute.zones().list(project=self.project).execute()

        self.zones = pyjq.all('.items[].name', result)

    def list_instances(self, compute, project, zone):
        result = compute.instances().list(project=project, zone=zone).execute()
        return result if 'items' in result else None

    def get_private_ip_addr(self, raw_describe_instances):
        return pyjq.all('.items[].networkInterfaces[].networkIP', raw_describe_instances)

    def get_public_ip_addr(self, raw_describe_instances):
        return pyjq.all('.items[].networkInterfaces[].accessConfigs[].natIP', raw_describe_instances)

    def save_result(self):
        now = datetime.now()

        timestamp = datetime.timestamp(now)
        file_name = "output/gcs_" + str(timestamp) + "_" + self.project + ".json"
        f = open(file_name, "a")
        data = {"public_ips": self.public_ips, "private_ips": self.private_ips}

        f.write(json.dumps(data, indent=4, sort_keys=True, default=str))
        f.close()
        print("*************************************************************************************")
        print("Data has been written to file : " + file_name + ". Please open the file to see result.")
        print("*************************************************************************************")


