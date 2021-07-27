import yaml
import json
from datetime import datetime
import digitalocean


class DO:
    config_file = ""
    env = ""
    do = ""
    public_ips = []

    def __init__(self, config_file):

        self.config_file = config_file

        stream = open(self.config_file, 'r')

        self.env = yaml.load(stream, Loader=yaml.FullLoader)

    def check_credentials(self):
        if self.env["digital-ocean"] is None:
            return "Error: no do configuratin found in " + self.config_file
        elif self.env["digital-ocean"]["token"] is None or self.env["digital-ocean"]["token"] is None \
                or self.env["digital-ocean"]["token"] is None or self.env["digital-ocean"]["token"] is None:
            return "Error: one of the required variable is not found in " + self.config_file + " e.g, (token)"
        else:
            self.do = self.env["digital-ocean"]
            return ""

    def start_scan(self):
        if self.check_credentials() != "":
            return self.check_credentials()
        bearer_token = self.env["digital-ocean"]["token"]

        manager = digitalocean.Manager(token=bearer_token)

        my_droplets = manager.get_all_droplets()

        self.get_public_ip_addr(my_droplets)

    def get_public_ip_addr(self, droplets):
        for droplet in droplets:
            # droplet.
            self.public_ips.append(droplet.ip_address)

    def save_result(self):

        now = datetime.now()

        timestamp = datetime.timestamp(now)
        file_name = "output/do_" + str(timestamp) + "_" + self.env["digital-ocean"]["token"] + ".json"
        f = open(file_name, "a")
        data = {"public_ips": self.public_ips}

        f.write(json.dumps(data, indent=4, sort_keys=True, default=str))
        f.close()
        print("*************************************************************************************")
        print("Data has been written to file : " + file_name + ". Please open the file to see result.")
        print("*************************************************************************************")
