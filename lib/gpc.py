from GPC import GPC
import yaml

stream = open("config.yaml", 'r')
config = yaml.load(stream, Loader=yaml.FullLoader)

project = config["gpc"]["token"]
gcs = GPC(project)
gcs.start_scan()
gcs.save_result()
