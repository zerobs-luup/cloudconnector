import yaml
import time
import http.client
import json
import pyjq
from datetime import datetime

class AZURE:
    config_file = ""
    env = ""
    azure = ""
    public_ips = []

    def __init__(self, config_file):

        self.config_file = config_file

        stream = open( self.config_file, 'r')

        # yaml_2 = YAML()
        # self.env = yaml_2.load(stream)
        # print(code)
        self.env = yaml.load(stream, Loader=yaml.FullLoader)

    def check_credentials(self):
        if self.env["azure"] is None:
            return "Error: no azure configuratin found in " + self.config_file
        elif self.env["azure"]["client-id"] is None or self.env["azure"]["client-secret"] is None \
                or self.env["azure"]["tenant-id"] is None or self.env["azure"]["subscription-id"] is None:
            return "Error: one of the required variable is not found in " + self.config_file + " e.g, (client-id, client-secret, tenant-id, subscription-id)"
        else:
            self.azure = self.env["azure"]
            return ""

    def start_scan(self):
        if self.check_credentials() != "":
            return self.check_credentials()
        bearer_token =  self.env["azure"]["bearer-token"]
        if self.env["azure"]["bearer-token"] is None or self.env["azure"]["bearer-expire-on"] is None or int(self.env["azure"]["bearer-expire-on"]) < datetime.now().timestamp():
            bearer_token = self.get_bearer_token()


        conn = http.client.HTTPSConnection("management.azure.com")
        payload = ''
        headers = {
                'Authorization': 'Bearer ' + bearer_token
            }
        conn.request("GET", "/subscriptions/" + self.env["azure"][
                "subscription-id"] + "/providers/Microsoft.Network/publicIPAddresses?api-version=2020-11-01", payload,
                         headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        self.public_ips = self.get_public_ip_addr(data)

    def get_bearer_token(self):

        conn = http.client.HTTPSConnection("login.microsoftonline.com")
        payload = 'grant_type=client_credentials&client_id=' + self.azure["client-id"] + '&client_secret=' + self.azure[
            "client-secret"] + '&resource=https://management.azure.com/'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'x-ms-gateway-slice=estsfd; stsservicecookie=estsfd; fpc=AjKuFqqZDJ5EohfWhz2Ut7A0z-1SAgAAAPihHdgOAAAA'
        }
        conn.request("POST", "/" + self.azure["tenant-id"] + "/oauth2/token", payload, headers)
        res = conn.getresponse()
        data = res.read()

        data = json.loads(data.decode("utf-8"))
        self.set_azure_val("bearer-token", data["access_token"])
        self.set_azure_val("bearer-expire-on", data["expires_on"])
        return data["access_token"]

    def set_azure_val(self, key, value):

        self.env['azure'][key] = value

        with open(self.config_file, 'w') as yaml_file:
            # self.env
            # YAML.dump()
            yaml_file.write(yaml.dump(self.env, default_flow_style=False))

    def get_public_ip_addr(self, raw_public_addr):
        return pyjq.all('.value[]|.properties.ipAddress', raw_public_addr)

    def save_result(self):

        now = datetime.now()

        timestamp = datetime.timestamp(now)
        file_name  = "output/azure_" + str(timestamp) + "_" + self.env["azure"]["client-id"] + ".json"
        f = open(file_name, "a")
        data = {"public_ips": self.public_ips}

        f.write(json.dumps(data, indent=4, sort_keys=True, default=str))
        f.close()
        print("*************************************************************************************")
        print("Data has been written to file : "+file_name + ". Please open the file to see result.")
        print("*************************************************************************************")


