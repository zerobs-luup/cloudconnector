#!venv/bin/python3
#
#
#

from DO import DO

do = DO("config.yaml")

do.start_scan()

do.save_result()
