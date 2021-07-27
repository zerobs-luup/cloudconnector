#!venv/bin/python3
#
#
#

from AZURE import AZURE

azure = AZURE("config.yaml")

azure.start_scan()

azure.save_result()




